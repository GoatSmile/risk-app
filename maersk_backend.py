import os
import pandas as pd
from datetime import datetime, timedelta, timezone
import requests
from typing import Dict, List, Tuple, Optional
import streamlit as st 
from newsapi import NewsApiClient
from nltk.sentiment import SentimentIntensityAnalyzer
from utils import parse_dt, logger, get_port_coordinates, load_port_geodata_with_details

# Add to imports
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import sqlite3
from contextlib import closing
from nltk.sentiment import SentimentIntensityAnalyzer
from maersk_backend import *
from sklearn.linear_model import LinearRegression
import spacy
from typing import Set

# Configuration
class Config:
    MAX_VESSELS = 300
    SEARCH_DAYS_BACK = 5 #ship schedule search days back
    API_TIMEOUT = 15
    DATE_RANGE = "P20D"
    BASE_URL = "https://api.maersk.com"
    STATUS_COLORS = {
        "en_route": [0, 255, 0, 160],
        "at_port": [255, 0, 0, 160]
    }
    NUMBER_ARTICLES_FETCH = 50
    RISK_HISTORY_DAYS = 30  # Add this line
    # NUMBER_SHIPS_FOR_WAVE_DATA = 5  
    WEATHER_FORECAST_DAYS = 7
    DB_PATH_FILE = "DB/maritime_risk.db"


# Marine Client
class MaerskClient:
    def __init__(self):
        logger.debug("Initializing Maersk client")
        if not os.getenv("MAERSK_CLIENT_ID"):
            raise ValueError("Missing MAERSK_CLIENT_ID environment variable")
            
        self.headers = {"Consumer-Key": os.getenv("MAERSK_CLIENT_ID")}

    def get_vessels(self) -> List[Dict]:
        response = requests.get(
            f"{Config.BASE_URL}/schedules/active-vessels",
            headers=self.headers,
            timeout=Config.API_TIMEOUT
        )
        response.raise_for_status()
        return self._filter_valid_vessels(response.json())

    def get_schedule(self, vessel_imo: str) -> Dict:
        params = {
            "vesselIMONumber": vessel_imo,
            "startDate": (datetime.now(timezone.utc) - timedelta(Config.SEARCH_DAYS_BACK)).strftime("%Y-%m-%d"),
            "dateRange": Config.DATE_RANGE,
            "carrierCodes": ["MAEU"]
        }
        try:
            response = requests.get(
                f"{Config.BASE_URL}/schedules/vessel-schedules",
                headers=self.headers,
                params=params,
                timeout=Config.API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {"vesselCalls": []}

    def _filter_valid_vessels(self, vessels: List[Dict]) -> List[Dict]:
        return [v for v in vessels if v.get("vesselIMONumber") and not pd.isna(v["vesselIMONumber"])]


def process_schedule(schedule: Dict) -> Tuple[Optional[Dict], List[Dict]]:
    now = datetime.now(timezone.utc)
    sorted_calls = sorted(schedule.get('vesselCalls', []), 
                         key=lambda vc: parse_dt(vc['callSchedules'][0]['classifierDateTime']))
    
    last_port = None
    for call in sorted_calls:
        arrival = parse_dt(call['callSchedules'][0]['classifierDateTime'])
        if arrival <= now:
            last_port = call
        else:
            break
            
    next_ports = sorted_calls[sorted_calls.index(last_port)+1:] if last_port else []
    
    return (
        get_port_details(last_port) if last_port else None,
        [get_port_details(p) for p in next_ports[:2] if p]
    )


def get_port_details(vessel_call: Dict) -> Optional[Dict]:
    if not vessel_call:
        return None
    
    facility = vessel_call.get('facility', {})
    unlocode = facility.get('UNLocationCode', '')
    lat, lon = get_port_coordinates(unlocode)
    
    # Handle missing coordinates
    lat = lat if lat is not None else 0.0
    lon = lon if lon is not None else 0.0
    
    # Debug zero coordinates
    if lat == 0.0 and lon == 0.0:
        logger.warning(f"Missing coordinates for {unlocode} - {facility.get('portName','Unknown')}")
    
    # Handle schedule parsing
    try:
        schedules = vessel_call['callSchedules']
        arrival = parse_dt(schedules[0]['classifierDateTime']).isoformat()
        departure = parse_dt(schedules[1]['classifierDateTime']).isoformat()
    except (KeyError, IndexError, TypeError):
        arrival = departure = "1970-01-01T00:00:00"  # Fallback value
    
    return {
        'port_name': facility.get('portName', 'Unknown'),
        'city': facility.get('cityName', ''),
        'country': facility.get('countryName', ''),
        'unlocode': unlocode,
        'lat': lat,
        'lon': lon,
        'arrival': arrival,
        'arrival': arrival,
        'departure': departure
    }
      

# ----------------
# NEWS SECTION
# ----------------

class NewsDB:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_PATH_FILE)
        self._create_tables()
        
    def _create_tables(self):
        with closing(self.conn.cursor()) as c:  
            c.execute('''
                CREATE TABLE IF NOT EXISTS articles
                (id TEXT PRIMARY KEY,
                 published DATETIME,
                 source TEXT,
                 title TEXT,
                 url TEXT UNIQUE,
                 sentiment REAL,
                 risk_keywords TEXT,
                 port_codes TEXT,
                 cities TEXT,
                 countries TEXT,
                 locations TEXT,
                 time_decay REAL,
                 wave_height REAL,
                 wind_speed REAL,
                 hist_risk REAL)
            ''')
            self.conn.commit()

    def save_article(self, article: Dict):
        with closing(self.conn.cursor()) as c:
            c.execute('''INSERT OR IGNORE INTO articles 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (
                        article['id'],
                        article['published'],
                        article['source'],
                        article['title'],
                        article['url'],
                        article['sentiment'],
                        ','.join(article['risk_keywords']),
                        ','.join(article['port_codes']),
                        ','.join(article['cities']),
                        ','.join(article['countries']),                        
                        ','.join(article['locations']),   
                        article['time_decay'],
                        article.get('wave_height', 0.0),
                        article.get('wind_speed', 0.0),
                        article.get('hist_risk', 0.0)
                    ))
            self.conn.commit()
        # Add temporary debug code to maersk_backend.py
        logger.debug(f"Saved article: {article['title']}")
    
        # except sqlite3.IntegrityError as e:
        #     logger.warning(f"Duplicate article: {article['id']}")



    def get_port_risk_trendsORIGIN(self, days=7):
        """Get time-decayed risk scores for ports"""
        with closing(self.conn.cursor()) as c:
            c.execute('''
                SELECT 
                    port_codes,
                    DATE(published) as date,
                    AVG(sentiment * time_decay) as decayed_risk
                FROM articles
                WHERE DATE(published) > DATE('now', ?)
                GROUP BY port_codes, date
                HAVING COUNT(*) > 1
                ORDER BY decayed_risk DESC
                LIMIT 10
            ''', (f'-{days} days',))  # Parameterized date modifier
            
            return pd.DataFrame(c.fetchall(), 
                            columns=['port_codes', 'date', 'decayed_risk'])


    # def get_port_risk_trends(self, days=7):
    #     """Return hardcoded sample risk data"""
    #     logger.debug("Returning sample risk data")
    #     return pd.DataFrame([('AESIN', '2025-02-08', 0.75)], 
    #                     columns=['port_codes', 'date', 'decayed_risk'])


    # def get_port_risk_trendsSAFE(self, days=7):
    #     """Get time-decayed risk scores for ports with default fallback"""
    #     default_date = datetime.now(timezone.utc).date().isoformat()
        
    #     try:
    #         with closing(self.conn.cursor()) as c:
    #             c.execute('''
    #                 SELECT 
    #                     port_codes,
    #                     DATE(published) as date,
    #                     AVG(sentiment * time_decay) as decayed_risk
    #                 FROM articles
    #                 WHERE DATE(published) > DATE('now', ?)
    #                 GROUP BY port_codes, date
    #                 HAVING COUNT(*) > 1
    #                 ORDER BY decayed_risk DESC
    #                 LIMIT 10
    #             ''', (f'-{days} days',))
                
    #             rows = c.fetchall()
                
    #             if not rows:  # No results found
    #                 logger.debug("Returning default risk trends")
    #                 return pd.DataFrame([('Unknown', default_date, 0.0)], 
    #                                 columns=['port_codes', 'date', 'decayed_risk'])
                
    #             return pd.DataFrame(rows, 
    #                             columns=['port_codes', 'date', 'decayed_risk'])
                                
    #     except Exception as e:
    #         logger.error(f"Risk trend error: {str(e)}")
    #         return pd.DataFrame([('Unknown', default_date, 0.0)], 
    #                         columns=['port_codes', 'date', 'decayed_risk'])


class EnhancedNewsClient:
    def __init__(self):
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            raise ValueError("NEWS_API_KEY environment variable is not set")
        self.api = NewsApiClient(api_key=api_key)

        logger.debug("Initialized News API client with API key")
        self.sia = SentimentIntensityAnalyzer()
        self.db = NewsDB()
        self.risk_keywords = {
            'piracy': 0.9, 'strike': 0.8, 'sanctions': 0.85,
            'storm': 0.7, 'blockade': 0.95, 'delay': 0.6
        }
        # Add to EnhancedNewsClient
        self.risk_factors = {
            'piracy': {'weight': 0.15, 'source': 'RiskIntelligenceAPI'},
            'sanctions': {'weight': 0.12, 'source': 'WindwardKYV'},
            'weather': {'weight': 0.18, 'source': 'DTNMarineWeather'},
            'port_congestion': {'weight': 0.10, 'source': 'PortLogAPI'}
        }     

        # Initialize NLP model
        self.nlp = spacy.load("en_core_web_sm")
        self.predictor = RiskPredictor()  # Add this line

    def calculate_combined_risk(self, article):
        """Integrate multiple risk factors"""
        base_score = article['sentiment'] * 0.7 + len(article['risk_keywords']) * 0.3
        return base_score * self.time_decay + sum(
            self.risk_factors[factor]['weight'] 
            for factor in article.get('external_risks', [])
        )

    def process_article(self, raw_article: Dict) -> Dict:
        """Enhanced processing with risk scoring"""
        # logger.debug(f"Processing article: {raw_article['title']}")
        processed = {
            'id': str(hash(f"{raw_article['title']}{raw_article['publishedAt']}")),
            'published': parse_dt(raw_article['publishedAt']).isoformat(),
            'source': raw_article['source']['name'],
            'title': raw_article['title'],
            'url': raw_article['url'],
            'risk_keywords': [],
            'port_codes': []
        }
        # logger.debug(f"Raw article: {processed['title']}")
        # Calculate time decay FIRST
        days_old = (datetime.now(timezone.utc) - 
                parse_dt(raw_article['publishedAt'])).days
        processed['time_decay'] = 0.95 ** days_old

        # Sentiment analysis
        content = f"{raw_article['title']}. {raw_article.get('description','')}"
        sentiment = self.sia.polarity_scores(content)
        processed['sentiment'] = sentiment['compound'] * -1  # Invert for risk

        # Keyword analysis
        content_lower = content.lower()
        processed['risk_keywords'] = [
            kw for kw in self.risk_keywords 
            if kw in content_lower
        ]


        # Port code detection with validation
        # ports = load_port_geodata()
        self.port_geo = load_port_geodata_with_details()
        
        entities_doc = self.nlp(content)
        # Extract locations
        locations = self._extract_locations(entities_doc)
        logger.debug(f"Extracted locations: {locations}")
        
        
        # Link locations to ports
        port_codes, cities, countries = self._link_to_ports(locations)
        
        processed.update({
            'port_codes': port_codes,
            'cities': cities,
            'countries': countries,
            'locations': locations
        })

        logger.debug(f"Processed features: {processed.keys()}")
        return processed
        
    def _extract_locations(self, doc) -> Set[str]:
        """Extract geographic entities from content"""
        return {
            ent.text.upper() for ent in doc.ents 
            if ent.label_ in ('GPE', 'LOC', 'FAC')
        }

    def _link_to_ports(self, locations: Set[str]) -> Tuple[List, Set, Set]:
        """Match extracted locations to UN/LOCODE database"""
        port_codes = []
        cities = set()
        countries = set()
        
        for loc in locations:
            # Check for direct port code match
            if loc in self.port_geo:
                port_codes.append(loc)
                cities.add(self.port_geo[loc]['city'])
                countries.add(self.port_geo[loc]['country'])
                continue
                
            # Check for city/country matches
            for code, data in self.port_geo.items():
                if loc == data['city'].upper() or loc == data['country'].upper():
                    port_codes.append(code)
                    cities.add(data['city'])
                    countries.add(data['country'])
        
        return list(set(port_codes)), cities, countries


    def get_and_save_news(self, num_articles: int) -> int:
        """Integrated fetch-and-save operation"""
        raw_articles = self.api.get_everything(
            q="maritime OR port OR shipping OR vessel OR cargo ship OR heist OR sea piracy",
            language="en",
            sort_by="publishedAt",
            page_size=num_articles
        ).get('articles', [])

        for raw in raw_articles:
            processed = self.process_article(raw)
            logger.debug(f"get_and_save_news----Processed article: {processed['title']}")
            self.db.save_article(processed)
        
        return len(raw_articles)


    def get_risk_history_df(self, days=30):
        """Get processed risk data for Streamlit"""
        df = pd.read_sql(f'''
            SELECT
                port_codes,
                DATE(published) as date,
                sentiment,
                time_decay,
                risk_keywords,
                AVG(wave_height) as wave_height,
                AVG(wind_speed) as wind_speed,
                AVG(hist_risk) as hist_risk,
                AVG(sentiment * time_decay) as decayed_risk,
                LEAD(AVG(hist_risk), 1) OVER (
                    PARTITION BY port_codes 
                    ORDER BY DATE(published)
                ) AS future_risk
            FROM articles
            WHERE DATE(published) > DATE('now', '-{days} days')
                GROUP BY port_codes, date
        ''', self.db.conn)
        
        # logger.debug(f"%%%%-Risk history data shape: {df.shape}") 
        # logger.debug(f"%%%%-Risk history data codes: {df['port_codes']}")
        if not df.empty:
            # Merge with port coordinates
            ports = load_port_geodata_with_details()

            # Create coordinate extraction with proper nested dict access
            df['lat'] = df['port_codes'].map(lambda x: ports.get(x.split(',')[0], {}).get('lat', 0) if x else 0)
            df['lon'] = df['port_codes'].map(lambda x: ports.get(x.split(',')[0], {}).get('lon', 0) if x else 0)                        
            df['future_risk'] = df['future_risk'].fillna(df['hist_risk'])
        return df

class RiskPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.features = [
            'hist_risk', 'wave_height', 'wind_speed', 
            'sentiment', 'time_decay'
        ]
        self.required_features = [
            'hist_risk', 'wave_height', 
            'wind_speed', 'sentiment', 'time_decay'
        ]
    def validate_features(self, df: pd.DataFrame) -> bool:
        logger.debug(f"Validating features: {df.columns}")

        required = self.required_features  # Separate features/target
        missing = [col for col in required if col not in df.columns]
        if missing:
            logger.error(f"Missing features: {missing}")
            return False
        return True

    def train(self, df: pd.DataFrame):
        if not self.validate_features(df):
            logger.error("Feature validation failed")
            return
    
        try:
            X = df[self.required_features].fillna(0)
            y = df['future_risk'].fillna(0)
            
            self.model.fit(X, y)
        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")

    def predict(self, X: pd.DataFrame) -> float:
        try:
            return max(0, min(self.model.predict(X)[0], 1))
        except: 
            return 0.0      


# ---------------- NEW SECTION ----------------
class OpenMeteoMarineClient:
    def __init__(self):
        self.base_url = "https://marine-api.open-meteo.com/v1/marine"
        self.session = requests.Session()
        
    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, max=20),
           retry=retry_if_exception_type(requests.exceptions.RequestException))
    
    def get_wave_forecast(self, lat: float, lon: float) -> Dict:
        logger.debug(f"get_wave_forecast: Requesting wave forecast for {lat}, {lon}")
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "wave_height_max",
                "forecast_days": Config.WEATHER_FORECAST_DAYS,
                "timezone": "UTC",
                "length_unit": "metric"
            }
            
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            return self._parse_response(response.json())
            
        except Exception as e:
            logger.error(f"OpenMeteo API failed: {str(e)}")
            return {}

    def _parse_response(self, data: Dict) -> Dict:
        """Extract daily max wave heights"""
        # logger.debug(f"_parse_response: OpenMeteo response: {data}")
        try:
            returndata = {
                'forecast': list(zip(
                    data['daily']['time'],
                    data['daily']['wave_height_max']
                )),
                'max': max(data['daily']['wave_height_max']),
                'average': sum(data['daily']['wave_height_max'])/len(data['daily']['wave_height_max'])
            }
            # logger.debug(f"_parse_response: OpenMeteo parsed data: {returndata}")
            return returndata
        except KeyError as e:
            logger.error(f"Missing key in response: {str(e)}")
            return {}
