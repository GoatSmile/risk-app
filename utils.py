import logging
from datetime import datetime, timezone
import pandas as pd
from typing import Dict, Tuple
from functools import lru_cache
from pathlib import Path
import time
import json


class ConfigUtils:
    # PORT_DATA_FILE = "UNLOCODE_port_list_1054_corrected_country_test.csv"
    PORT_DATA_FILE = "data/UNLOCODE_port_list_1054_corrected_country.csv"

def configure_logging():
    """One-time logging setup"""
    logger = logging.getLogger("MaerskMonitor")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent duplicate logs
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)
    
    return logger

# Initialize logger instance
logger = configure_logging()
   
# Data processing
class PortDataCache:
    """Cache manager for port data with file modification monitoring."""
    
    _instance = None
    CACHE_FILE = "data/.port_cache.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._last_mtime = 0
            self._cache = {}
            self._load_cache()
    
    def _get_csv_mtime(self) -> float:
        """Get the modification time of the port data CSV file."""
        try:
            return Path(ConfigUtils.PORT_DATA_FILE).stat().st_mtime
        except OSError:
            return 0
    
    def _load_cache(self):
        """Load cached data from disk if available."""
        try:
            cache_path = Path(self.CACHE_FILE)
            if cache_path.exists():
                with cache_path.open('r') as f:
                    cached_data = json.load(f)
                    self._last_mtime = cached_data.get('mtime', 0)
                    self._cache = cached_data.get('data', {})
                    logger.info("Loaded port data from cache")
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
    
    def _save_cache(self):
        """Save current cache to disk."""
        try:
            cache_path = Path(self.CACHE_FILE)
            cache_path.parent.mkdir(exist_ok=True)
            with cache_path.open('w') as f:
                json.dump({
                    'mtime': self._last_mtime,
                    'data': self._cache
                }, f)
            logger.info("Saved port data to cache")
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def _needs_refresh(self) -> bool:
        """Check if cache needs to be refreshed."""
        current_mtime = self._get_csv_mtime()
        return current_mtime > self._last_mtime
    
    def _load_from_csv(self) -> Dict:
        """Load data directly from CSV file."""
        try:
            df = pd.read_csv(ConfigUtils.PORT_DATA_FILE)
            
            # Process basic geodata
            geodata = {
                str(row["UNLOCODE"]).strip().upper()[:5]: (float(row["LAT"]), float(row["LON"]))
                for _, row in df.iterrows()
            }
            
            # Process detailed data
            detailed_data = {
                row['UNLOCODE']: {
                    'lat': float(row['LAT']),
                    'lon': float(row['LON']),
                    'city': row['PORT_NAME'],
                    'country': row['COUNTRY']
                }
                for _, row in df.iterrows()
            }
            
            self._cache = {
                'geodata': geodata,
                'detailed_data': detailed_data,
                'last_refresh': time.time()
            }
            
            self._last_mtime = self._get_csv_mtime()
            self._save_cache()
            
            logger.info("Refreshed port data from CSV")
            return self._cache
            
        except Exception as e:
            logger.error(f"Failed to load port data from CSV: {e}")
            return {}
    
    def get_data(self, detailed: bool = False) -> Dict:
        """Get port data, refreshing from CSV if needed."""
        if self._needs_refresh() or not self._cache:
            self._load_from_csv()
        
        if not self._cache:
            return {}
            
        return self._cache['detailed_data'] if detailed else self._cache['geodata']

@lru_cache(maxsize=1)
def load_port_geodata() -> Dict[str, Tuple[float, float]]:
    """Load basic port geodata with caching."""
    return PortDataCache().get_data(detailed=False)

@lru_cache(maxsize=1)
def load_port_geodata_with_details() -> Dict:
    """Load detailed port data with caching."""
    return PortDataCache().get_data(detailed=True)

def refresh_port_data():
    """Force refresh of port data cache."""
    load_port_geodata.cache_clear()
    load_port_geodata_with_details.cache_clear()
    PortDataCache()._load_from_csv()

def get_cache_stats() -> Dict:
    """Get cache statistics for monitoring."""
    cache = PortDataCache()
    return {
        'cache_size': len(cache._cache),
        'last_refresh': cache._cache.get('last_refresh'),
        'file_mtime': cache._last_mtime,
        'needs_refresh': cache._needs_refresh()
    }

# @st.cache_data(ttl=3600)
def get_port_coordinates(unlocode):
    """Safe coordinate retrieval with validation"""
    try:
        if not unlocode or pd.isna(unlocode):
            return None, None
            
        code = str(unlocode).strip().upper()[:5]
        if len(code) != 5:
            logger.warning(f"Invalid UN/LOCODE: {unlocode}")
            return None, None
            
        ports = load_port_geodata()
        if code not in ports:
            logger.warning(f"UN/LOCODE {code} not found in the list of ports")
            return None, None
            
        return float(ports[code][0]), float(ports[code][1])
    except Exception as e:
        logger.error(f"Coordinate error: {str(e)}")
        return None, None


def parse_dt(dt_str: str) -> datetime:
    """Parse datetime string to UTC datetime object.
    
    Args:
        dt_str: ISO format datetime string
        
    Returns:
        datetime: UTC datetime object
        
    Raises:
        ValueError: If datetime string is invalid
    """
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.astimezone(timezone.utc)
    except ValueError as e:
        logger.error(f"Failed to parse datetime: {dt_str}")
        raise ValueError(f"Invalid datetime format: {dt_str}") from e