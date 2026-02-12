"""
Data Loader for jgt-data-server Integration

Provides data access from jgt-data-server API for regime detection and signal scoring.
"""

import os
import logging
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import requests


class DataLoader:
    """
    Load market data from jgt-data-server or local files.
    
    Supports:
    - jgt-data-server REST API
    - Local file system (fallback)
    - Environment variable configuration
    """
    
    def __init__(
        self,
        data_server_url: Optional[str] = None,
        local_data_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize data loader.
        
        Args:
            data_server_url: URL of jgt-data-server (env: JGT_DATA_SERVER_URL)
            local_data_path: Path to local data files (env: JGTPY_DATA)
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("DataLoader")
        
        # Get data server URL from env or param
        self.data_server_url = data_server_url or os.getenv(
            "JGT_DATA_SERVER_URL",
            "http://localhost:5555"
        )
        
        # Get local data path from env or param
        self.local_data_path = local_data_path or os.getenv(
            "JGTPY_DATA",
            "/src/jgtml/data"
        )
        
        self.logger.info(f"[DataLoader] Initialized - Server: {self.data_server_url}, Local: {self.local_data_path}")
    
    def load_cds(
        self,
        instrument: str,
        timeframe: str,
        dataset: str = "current"
    ) -> Optional[pd.DataFrame]:
        """
        Load CDS (signal) data for an instrument.
        
        Args:
            instrument: Instrument name (e.g., 'EUR-USD')
            timeframe: Timeframe (e.g., 'H4', 'D1')
            dataset: Dataset name ('current' or 'discovery')
        
        Returns:
            DataFrame with CDS data or None
        """
        # Try API first
        df = self._load_from_api(instrument, timeframe, "cds", dataset)
        
        # Fallback to local files
        if df is None:
            df = self._load_from_local(instrument, timeframe, "cds", dataset)
        
        return df
    
    def load_pds(
        self,
        instrument: str,
        timeframe: str,
        dataset: str = "current"
    ) -> Optional[pd.DataFrame]:
        """
        Load PDS (price) data for an instrument.
        
        Args:
            instrument: Instrument name
            timeframe: Timeframe
            dataset: Dataset name
        
        Returns:
            DataFrame with PDS data or None
        """
        df = self._load_from_api(instrument, timeframe, "pds", dataset)
        if df is None:
            df = self._load_from_local(instrument, timeframe, "pds", dataset)
        return df
    
    def load_ttf(
        self,
        instrument: str,
        timeframe: str,
        dataset: str = "current"
    ) -> Optional[pd.DataFrame]:
        """
        Load TTF (cross-timeframe features) data.
        
        Args:
            instrument: Instrument name
            timeframe: Timeframe
            dataset: Dataset name
        
        Returns:
            DataFrame with TTF data or None
        """
        df = self._load_from_api(instrument, timeframe, "ttf", dataset)
        if df is None:
            df = self._load_from_local(instrument, timeframe, "ttf", dataset)
        return df
    
    def _load_from_api(
        self,
        instrument: str,
        timeframe: str,
        data_type: str,
        dataset: str
    ) -> Optional[pd.DataFrame]:
        """Load data from jgt-data-server API."""
        try:
            url = f"{self.data_server_url}/market-data"
            params = {
                "instrument": instrument,
                "timeframe": timeframe,
                "data_type": data_type,
                "dataset": dataset
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("data"):
                    df = pd.DataFrame(data["data"])
                    self.logger.info(f"[DataLoader] Loaded {data_type} from API: {instrument} {timeframe}")
                    return df
            
            self.logger.warning(f"[DataLoader] API load failed: {response.status_code}")
            return None
            
        except Exception as e:
            self.logger.warning(f"[DataLoader] API error: {e}")
            return None
    
    def _load_from_local(
        self,
        instrument: str,
        timeframe: str,
        data_type: str,
        dataset: str
    ) -> Optional[pd.DataFrame]:
        """Load data from local file system."""
        try:
            # Normalize instrument name for file path
            inst_normalized = instrument.replace('/', '-').replace('_', '-')
            
            # Build file path
            file_path = Path(self.local_data_path) / dataset / data_type / f"{inst_normalized}-{timeframe}.csv"
            
            if file_path.exists():
                df = pd.read_csv(file_path)
                self.logger.info(f"[DataLoader] Loaded {data_type} from file: {file_path}")
                return df
            else:
                self.logger.warning(f"[DataLoader] File not found: {file_path}")
                return None
                
        except Exception as e:
            self.logger.error(f"[DataLoader] Local load error: {e}")
            return None
