UAODS
EGPSE

D7Q9Bam2q6mU9D8pRj1H87xoH1BU4FlV

4PF8BP-as8pwwUKssuupvZc7soX5nND8dmcaYwd5xPofkKqLyL3kY5seOXnOfEkE



CREATE TABLE articles (
    id TEXT PRIMARY KEY,
    published DATETIME,
    source TEXT,
    title TEXT,
    url TEXT UNIQUE,
    sentiment REAL,
    risk_keywords TEXT,
    port_codes TEXT,
    time_decay REAL,
    wave_height REAL,  -- Maps to significantWaveHeight
    wind_speed REAL,   -- Maps to windSpeed10m
    hist_risk REAL     -- Can be deprecated later
);


# Test authentication separately
python3 -c """
import os
import requests
print(requests.post(
    'https://https://api.auth.dtn.com/v1/tokens/authorize',
    data={
        'grant_type': 'client_credentials',
        'client_id': os.getenv('DTN_CLIENT_ID'),
        'client_secret': os.getenv('DTN_CLIENT_SECRET'),
        'audience': 'https://api.dtn.com/marine'
    },
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
).json())
"""


https://api.auth.dtn.com/v1/tokens/authorize


https://weather.api.dtn.com/v1/conditions/marine?lat=0.0&lon=0.0&startTime=2025-02-08T22%3A02%3A23%2B00%3A00&parameters=significantWaveHeight%2CwindSpeed10m%2CseaSurfaceTemp

python3 -c "from dotenv import load_dotenv; load_dotenv(); import conn.py"


curl -X POST https://api.auth.dtn.com/v1/tokens/authorize \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "'"HtEwHh9beCoipSTnqrVm0rolv1TGBOHb"'",
    "client_secret": "'"-lK8DxtEw0CQPqaJjX6RcRpbmIh9OX9ucXKQxR9_XEBj1syoJr4FYN-nZ1gZAxRj"'", 
    "audience": "https://weather.api.dtn.com/conditions"
  }'


  auth_url = 'https://api.auth.dtn.com/v1/tokens/authorize'

  body = {
      'grant_type': 'client_credentials',
      'client_id': '...insert your client id here...',
      'client_secret': '...insert your client secret here...',
      'audience': 'https://weather.api.dtn.com/conditions/marine'
  }

WORKED

curl -X POST https://api.auth.dtn.com/v1/tokens/authorize \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "'"HtEwHh9beCoipSTnqrVm0rolv1TGBOHb"'",
    "client_secret": "'"-lK8DxtEw0CQPqaJjX6RcRpbmIh9OX9ucXKQxR9_XEBj1syoJr4FYN-nZ1gZAxRj"'", 
    "audience": "https://weather.api.dtn.com/conditions/marine"
  }'

https://weather.api.dtn.com/conditions/marine

{"error":{"message":"Client is not authorized to access \"https://weather.api.dtn.com/conditions\". You need to create a \"client-grant\" associated to this API. See: https://auth0.com/docs/api/management/v2/client-grants/post-client-grants","status":403,"code":"access_denied"},"meta":{"type":"authentication","date_time":"2025-02-08T20:45:20.264Z","name":"v1.tokens.authorize","uuid":"b4426c8f-b2da-4224-81d0-72592f06f10e","request_id":"b4426c8f-b2da-4224-81d0-72592f06f10e","start_timestamp":1739047520166,"end_timestamp":1739047520265,"execution_time":99}}(risk-env) nt@NT-Mac risk-app % 

curl -v https://weather.api.dtn.com/v1/conditions/marine

https://api.auth.dtn.com/v1/tokens/authorize

curl -v https://weather.api.dtn.com/v2/conditions

# Create empty database
sqlite3 maritime_risk.db "VACUUM;"

# Test database structure
sqlite3 maritime_risk.db ".schema"

# Delete existing database to force recreation
rm maritime_risk.db

# Restart the application
streamlit run risk-app-p.py


sqlite3 maritime_risk.db ".schema articles"




----

# Install missing dependency
pip install sqlite3

# Start the app (from existing setup)
streamlit run risk-app-p.py


graph TD
    A[Maersk API] --> B{Vessel Data}
    C[News API] --> D{News Analysis}
    E[Weather API] --> F{Weather Risks}
    G[Port Database] --> H{Port Risks}
    B --> I[Risk Engine]
    D --> I
    F --> I
    H --> I
    I --> J[Dashboard]
    J --> K[Interactive Map]
    J --> L[Risk Heatmaps]
    J --> M[Predictive Analytics]



+-----------------------+
|  Real-Time Risk Map   |
+-----------+-----------+
| Risk Heatmap | Alert |
| (Regional)  | Feed   |
+-----------+-----------+
| Predictive Analytics |
| (Time Series)        |
+----------------------+

News API → Entity Extraction → Geo-Tagging → Sentiment Analysis → Risk Scoring → TimescaleDB


# New risk assessment structure
class RiskAssessor:
    def __init__(self):
        self.base_risk = {
            'port': 0.5,  # From port database
            'country': 0.3,  # From World Bank API
            'weather': 0.0,  # From NOAA API
            'sentiment': 0.2  # From news analysis
        }
        
    def calculate_risk(self, vessel_data):
        # Implement time decay factor for historical data
        time_decay = 0.95 ** (days_since_incident)  # Customizable decay rate
        return sum([
            self.base_risk['port'] * port_risk_factor,
            self.base_risk['country'] * country_risk,
            self.base_risk['weather'] * weather_impact,
            self.base_risk['sentiment'] * news_sentiment
        ]) * time_decay


# Add to maersk_backend.py
class RiskHistory:
    def __init__(self):
        self.history = {}  # {port_code: {date: risk_score}}
        
    def add_data(self, port_code, risk_score):
        today = datetime.now().date()
        self.history.setdefault(port_code, {})
        self.history[port_code][today] = risk_score
        
    def get_trend(self, port_code, window=30):
        # Calculate moving average with time decay
        port_data = self.history.get(port_code, {})
        recent = [v * (0.95 ** i) for i, v in enumerate(port_data.values())]
        return sum(recent[:window]) / window if recent else 0


# Modify NewsClient in maersk_backend.py
class EnhancedNewsClient(NewsClient):
    def __init__(self):
        super().__init__()
        self.risk_keywords = {
            'strike': 0.8,
            'piracy': 0.9,
            'storm': 0.7,
            'sanctions': 0.85
        }
    
    def analyze_article(self, text):
        # Combine semantic analysis with keyword scoring
        sentiment = self.sia.polarity_scores(text)
        keyword_score = sum(
            self.risk_keywords.get(word.lower(), 0) 
            for word in text.split()
        )
        return (sentiment['compound'] * -0.5) + (keyword_score * 0.5)


# Modify risk-app-p.py visualization
def create_enhanced_map(positions, risk_data):
    return pdk.Deck(
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=risk_data,
                get_position=['lon', 'lat'],
                aggregation=pdk.types.String("MEAN"),
                get_weight="risk_score",
                radius=20000
            ),
            # Existing vessel layers
        ]
    )


class EnhancedNewsClient(NewsClient):
    def process_article(self, raw: Dict) -> Dict:
        return {
            'headline': raw['title'],
            'url': raw['url'],
            'published': parse_dt(raw['publishedAt']),
            'entities': self.extract_entities(raw['content']),
            'risk_score': self.calculate_risk_score(raw),
            'geo': self.geotag_article(raw['content'])
        }
    
    def extract_entities(self, text: str) -> Dict:
        """Match UN/LOCODEs and IMOs using your existing datasets"""
        return {
            'ports': [code for code in PORT_CODES if code in text],
            'vessels': [imo for imo in VESSEL_IMOS if imo in text]
        }
