# %%
# Grafana Integration for ADS-B Trajectory Visualization
# Enhanced version of tests5_clean.py with Grafana export capabilities

import gzip
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyproj
from shapely.geometry import LineString, Point

# Database imports for Grafana integration
try:
    from influxdb_client import InfluxDBClient, Point as InfluxPoint, WritePrecision
    from influxdb_client.client.write_api import SYNCHRONOUS
    INFLUXDB_AVAILABLE = True
except ImportError:
    INFLUXDB_AVAILABLE = False
    print("InfluxDB client not available. Install with: pip install influxdb-client")

try:
    import psycopg2
    from sqlalchemy import create_engine
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False
    print("PostgreSQL client not available. Install with: pip install psycopg2-binary sqlalchemy")

# Configuration for Grafana integration
GRAFANA_CONFIG = {
    'influxdb': {
        'url': 'http://localhost:8086',
        'token': 'your-influxdb-token',
        'org': 'your-org',
        'bucket': 'adsb-trajectories'
    },
    'postgresql': {
        'host': 'localhost',
        'port': 5432,
        'database': 'adsb_db',
        'user': 'postgres',
        'password': 'your-password'
    }
}

# Utility functions from original file
def iterate_time(data, threshold):
    """Split data by time gaps larger than threshold seconds"""
    # Ensure timestamp is datetime type
    if not pd.api.types.is_datetime64_any_dtype(data['timestamp']):
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    
    idx = np.where(data.timestamp.diff().dt.total_seconds() > threshold)[0]
    start = 0
    for stop in idx:
        yield data.iloc[start:stop]
        start = stop + 1
    yield data.iloc[start:]

def iterate_icao24_callsign(data):
    """Group data by ICAO24 and callsign"""
    for _, chunk in data.groupby(["icao24", "callsign"]):
        yield chunk

class GrafanaExporter:
    """Handles data export to Grafana-compatible databases"""
    
    def __init__(self, config: Dict = None):
        self.config = config or GRAFANA_CONFIG
        self.influx_client = None
        self.postgres_engine = None
        
        if INFLUXDB_AVAILABLE:
            self._init_influxdb()
        if POSTGRESQL_AVAILABLE:
            self._init_postgresql()
    
    def _init_influxdb(self):
        """Initialize InfluxDB connection"""
        try:
            self.influx_client = InfluxDBClient(
                url=self.config['influxdb']['url'],
                token=self.config['influxdb']['token'],
                org=self.config['influxdb']['org']
            )
            print("InfluxDB connection initialized")
        except Exception as e:
            print(f"Failed to initialize InfluxDB: {e}")
    
    def _init_postgresql(self):
        """Initialize PostgreSQL connection"""
        try:
            pg_config = self.config['postgresql']
            connection_string = f"postgresql://{pg_config['user']}:{pg_config['password']}@{pg_config['host']}:{pg_config['port']}/{pg_config['database']}"
            self.postgres_engine = create_engine(connection_string)
            print("PostgreSQL connection initialized")
        except Exception as e:
            print(f"Failed to initialize PostgreSQL: {e}")
    
    def export_trajectory_to_influx(self, flight_data: pd.DataFrame, flight_id: str):
        """Export trajectory points to InfluxDB for time-series visualization"""
        if not self.influx_client:
            print("InfluxDB not available")
            return False
        
        try:
            write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
            points = []
            
            for _, row in flight_data.iterrows():
                point = (
                    InfluxPoint("trajectory")
                    .tag("flight_id", flight_id)
                    .tag("icao24", row.get('icao24', ''))
                    .tag("callsign", row.get('callsign', ''))
                    .field("latitude", float(row['latitude']))
                    .field("longitude", float(row['longitude']))
                    .field("altitude", float(row.get('altitude', 0)))
                    .field("vertical_rate", float(row.get('vertical_rate', 0)))
                    .field("ground_speed", float(row.get('ground_speed', 0)))
                    .time(int(row['timestamp']), WritePrecision.S)
                )
                points.append(point)
            
            write_api.write(bucket=self.config['influxdb']['bucket'], record=points)
            print(f"Exported {len(points)} points to InfluxDB for flight {flight_id}")
            return True
            
        except Exception as e:
            print(f"Error exporting to InfluxDB: {e}")
            return False
    
    def export_flight_metadata_to_postgres(self, flight_summary: Dict):
        """Export flight metadata to PostgreSQL"""
        if not self.postgres_engine:
            print("PostgreSQL not available")
            return False
        
        try:
            df = pd.DataFrame([flight_summary])
            df.to_sql('flight_metadata', self.postgres_engine, if_exists='append', index=False)
            print(f"Exported flight metadata for {flight_summary.get('flight_id')}")
            return True
            
        except Exception as e:
            print(f"Error exporting to PostgreSQL: {e}")
            return False

class FlightGrafana:
    """Enhanced Flight class with Grafana export capabilities"""
    
    def __init__(self, data: pd.DataFrame, exporter: GrafanaExporter = None):
        self.data = data
        self.exporter = exporter
        self._trajectory_cache = None
    
    def __repr__(self):
        return (
            f"FlightGrafana {self.callsign} with aircraft {self.icao24} "
            f"on {self.min('timestamp'):%Y-%m-%d}"
        )
    
    def __lt__(self, other):
        return self.min("timestamp") <= other.min("timestamp")
    
    def max(self, feature):
        if feature == "timestamp":
            # Ensure timestamp is datetime type
            if not pd.api.types.is_datetime64_any_dtype(self.data[feature]):
                return pd.to_datetime(self.data[feature], unit='s').max()
        return self.data[feature].max()

    def min(self, feature):
        if feature == "timestamp":
            # Ensure timestamp is datetime type
            if not pd.api.types.is_datetime64_any_dtype(self.data[feature]):
                return pd.to_datetime(self.data[feature], unit='s').min()
        # For string features, ensure we get the first non-null value
        if feature in ["callsign", "icao24"]:
            return self.data[feature].dropna().iloc[0] if len(self.data[feature].dropna()) > 0 else None
        return self.data[feature].min()
    
    @property
    def callsign(self):
        return self.min("callsign")
    
    @property
    def icao24(self):
        return self.min("icao24")
    
    @property
    def flight_id(self):
        """Generate unique flight ID for Grafana"""
        start_time = self.min("timestamp").strftime("%Y%m%d_%H%M%S")
        return f"{self.icao24}_{self.callsign}_{start_time}"
    
    def altitude_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Return (alt_min, alt_max) for this flight"""
        alt_data = pd.to_numeric(self.data["altitude"], errors='coerce').dropna()
        if len(alt_data) == 0:
            return None, None
        return alt_data.min(), alt_data.max()
    
    def vertical_rate_range(self) -> Tuple[Optional[float], Optional[float]]:
        """Return (vr_min, vr_max) for this flight"""
        vr_data = pd.to_numeric(self.data["vertical_rate"], errors='coerce').dropna()
        if len(vr_data) == 0:
            return None, None
        return vr_data.min(), vr_data.max()
    
    def is_landing(self, ground_altitude_threshold=100, descent_rate_threshold=-1500) -> bool:
        """Determine if flight is a landing"""
        alt_min, alt_max = self.altitude_range()
        vr_min, vr_max = self.vertical_rate_range()
        
        if alt_min is None or vr_min is None:
            return False
        
        return alt_min <= ground_altitude_threshold and vr_min <= descent_rate_threshold
    
    def is_takeoff(self, ground_altitude_threshold=100, climb_rate_threshold=3000) -> bool:
        """Determine if flight is a takeoff"""
        alt_min, alt_max = self.altitude_range()
        vr_min, vr_max = self.vertical_rate_range()
        
        if alt_min is None or vr_max is None:
            return False
        
        return alt_min <= ground_altitude_threshold and vr_max >= climb_rate_threshold
    
    def get_trajectory(self) -> pd.DataFrame:
        """Return trajectory coordinates with timestamp"""
        if self._trajectory_cache is not None:
            return self._trajectory_cache
        
        # Select available columns, ground_speed is optional
        available_columns = ["latitude", "longitude", "altitude", "timestamp", "vertical_rate"]
        if "ground_speed" in self.data.columns:
            available_columns.append("ground_speed")
        
        trajectory = (
            self.data[available_columns]
            .dropna(subset=["latitude", "longitude", "altitude"])
            .copy()
        )
        
        if len(trajectory) > 0:
            trajectory["timestamp_dt"] = pd.to_datetime(
                trajectory["timestamp"], unit="s"
            )
            trajectory = trajectory.sort_values("timestamp_dt")
        
        self._trajectory_cache = trajectory
        return trajectory
    
    def has_valid_trajectory(self) -> bool:
        """Check if flight has valid trajectory"""
        return len(self.get_trajectory()) > 1
    
    def get_flight_summary(self) -> Dict:
        """Generate flight summary for Grafana metadata"""
        trajectory = self.get_trajectory()
        alt_min, alt_max = self.altitude_range()
        vr_min, vr_max = self.vertical_rate_range()
        
        return {
            'flight_id': self.flight_id,
            'icao24': self.icao24,
            'callsign': self.callsign,
            'start_time': self.min("timestamp"),
            'end_time': self.max("timestamp"),
            'duration_minutes': (self.max("timestamp") - self.min("timestamp")).total_seconds() / 60,
            'total_points': len(trajectory),
            'altitude_min': alt_min,
            'altitude_max': alt_max,
            'vertical_rate_min': vr_min,
            'vertical_rate_max': vr_max,
            'is_landing': self.is_landing(),
            'is_takeoff': self.is_takeoff(),
            'start_lat': trajectory.iloc[0]['latitude'] if len(trajectory) > 0 else None,
            'start_lon': trajectory.iloc[0]['longitude'] if len(trajectory) > 0 else None,
            'end_lat': trajectory.iloc[-1]['latitude'] if len(trajectory) > 0 else None,
            'end_lon': trajectory.iloc[-1]['longitude'] if len(trajectory) > 0 else None,
        }
    
    def export_to_grafana(self) -> bool:
        """Export flight data to Grafana databases"""
        if not self.exporter:
            print("No Grafana exporter configured")
            return False
        
        trajectory = self.get_trajectory()
        if len(trajectory) == 0:
            print(f"No trajectory data for flight {self.flight_id}")
            return False
        
        # Export trajectory points to InfluxDB
        influx_success = self.exporter.export_trajectory_to_influx(trajectory, self.flight_id)
        
        # Export metadata to PostgreSQL
        flight_summary = self.get_flight_summary()
        postgres_success = self.exporter.export_flight_metadata_to_postgres(flight_summary)
        
        return influx_success and postgres_success
    
    def to_geopandas(self, transformer=None):
        """Convert trajectory to GeoDataFrame (from original implementation)"""
        trajectory = self.get_trajectory()
        if len(trajectory) == 0:
            return None
        
        if transformer is None:
            transformer = pyproj.Transformer.from_crs(
                "EPSG:4326", "EPSG:2154", always_xy=True
            )
        
        # Convert coordinates
        x_coords, y_coords = transformer.transform(
            trajectory["longitude"].values, trajectory["latitude"].values
        )
        
        # Filter outliers (Paris region)
        center_x, center_y = 650000, 6860000
        max_distance = 100000
        
        valid_mask = (abs(x_coords - center_x) <= max_distance) & (
            abs(y_coords - center_y) <= max_distance
        )
        
        if not valid_mask.any():
            return None
        
        # Create GeoDataFrame with points and line
        trajectory_filtered = trajectory[valid_mask].copy()
        x_filtered = x_coords[valid_mask]
        y_filtered = y_coords[valid_mask]
        
        trajectory_filtered["x_lambert"] = x_filtered
        trajectory_filtered["y_lambert"] = y_filtered
        trajectory_filtered["geometry"] = [
            Point(x, y) for x, y in zip(x_filtered, y_filtered)
        ]
        
        gdf = gpd.GeoDataFrame(trajectory_filtered, crs="EPSG:2154")
        
        # Add trajectory line
        if len(gdf) > 1:
            coords = [(row.x_lambert, row.y_lambert) for _, row in gdf.iterrows()]
            line_gdf = gpd.GeoDataFrame(
                [{"icao24": self.icao24, "geometry": LineString(coords)}],
                crs="EPSG:2154",
            )
            return gdf, line_gdf
        
        return gdf, None

class FlightCollectionGrafana:
    """Enhanced FlightCollection with Grafana integration"""
    
    def __init__(self, data: pd.DataFrame, exporter: GrafanaExporter = None):
        self.data = data
        self.exporter = exporter or GrafanaExporter()
    
    def __repr__(self):
        return f"FlightCollectionGrafana with {len(self)} flights"
    
    @classmethod
    def read_json(cls, filename: str, exporter: GrafanaExporter = None):
        """Read JSON file and create collection"""
        return cls(pd.read_json(filename), exporter)
    
    @classmethod
    def read_jsonl_gz(cls, filename: str, exporter: GrafanaExporter = None):
        """Read compressed JSONL file and create collection"""
        data = []
        with gzip.open(filename, "rt", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.strip():
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        df = pd.DataFrame(data)
        
        # Preprocess timestamp column if it exists
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Convert numeric columns to proper types
        if 'altitude' in df.columns:
            df['altitude'] = pd.to_numeric(df['altitude'], errors='coerce')
        if 'vertical_rate' in df.columns:
            df['vertical_rate'] = pd.to_numeric(df['vertical_rate'], errors='coerce')
        
        return cls(df, exporter)
    
    def __iter__(self):
        for group in iterate_icao24_callsign(self.data):
            for elt in iterate_time(group, 20000):
                yield FlightGrafana(elt, self.exporter)
    
    def __len__(self):
        return sum(1 for _ in self)
    
    def __getitem__(self, key):
        if isinstance(key, str):
            result = FlightCollectionGrafana(
                self.data.query("callsign == @key or icao24 == @key"),
                self.exporter
            )
        if isinstance(key, pd.Timestamp):
            before = key
            after = key + timedelta(days=1)
            result = FlightCollectionGrafana(
                self.data.query("@before < timestamp < @after"),
                self.exporter
            )
        
        if len(result) == 1:
            return FlightGrafana(result.data, self.exporter)
        else:
            return result
    
    def filter_by_icao24_only(self):
        """Iterate over flights grouped by icao24 only"""
        for icao24, group in self.data.groupby("icao24"):
            if len(group) > 1:
                yield FlightGrafana(group, self.exporter)
    
    def filter_landings(self) -> List[FlightGrafana]:
        """Return landing flights"""
        landings = []
        for flight in self.filter_by_icao24_only():
            if flight.is_landing() and flight.has_valid_trajectory():
                landings.append(flight)
        return landings
    
    def filter_takeoffs(self) -> List[FlightGrafana]:
        """Return takeoff flights"""
        takeoffs = []
        for flight in self.filter_by_icao24_only():
            if flight.is_takeoff() and flight.has_valid_trajectory():
                takeoffs.append(flight)
        return takeoffs
    
    def get_statistics(self) -> Dict:
        """Return collection statistics"""
        total_flights = 0
        landings = 0
        takeoffs = 0
        
        for flight in self.filter_by_icao24_only():
            total_flights += 1
            if flight.is_landing():
                landings += 1
            if flight.is_takeoff():
                takeoffs += 1
        
        return {
            "total_flights": total_flights,
            "landings": landings,
            "takeoffs": takeoffs,
        }
    
    def export_all_to_grafana(self, max_flights: int = None) -> Dict:
        """Export all flights to Grafana databases"""
        results = {
            'exported': 0,
            'failed': 0,
            'skipped': 0
        }
        
        flights = list(self.filter_by_icao24_only())
        if max_flights:
            flights = flights[:max_flights]
        
        print(f"Exporting {len(flights)} flights to Grafana...")
        
        for i, flight in enumerate(flights):
            if not flight.has_valid_trajectory():
                results['skipped'] += 1
                continue
            
            try:
                if flight.export_to_grafana():
                    results['exported'] += 1
                else:
                    results['failed'] += 1
                
                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1}/{len(flights)} flights")
                    
            except Exception as e:
                print(f"Error exporting flight {flight.flight_id}: {e}")
                results['failed'] += 1
        
        print(f"Export complete: {results['exported']} exported, {results['failed']} failed, {results['skipped']} skipped")
        return results
    
    def stream_to_grafana(self, interval_seconds: int = 60):
        """Stream flight data to Grafana in real-time simulation"""
        print(f"Starting real-time streaming to Grafana (interval: {interval_seconds}s)")
        
        flights = list(self.filter_by_icao24_only())
        
        for flight in flights:
            if not flight.has_valid_trajectory():
                continue
            
            print(f"Streaming flight {flight.flight_id}")
            trajectory = flight.get_trajectory()
            
            # Stream points one by one to simulate real-time
            for _, point in trajectory.iterrows():
                point_df = pd.DataFrame([point])
                if self.exporter:
                    self.exporter.export_trajectory_to_influx(point_df, flight.flight_id)
                
                time.sleep(interval_seconds / len(trajectory))
            
            # Export metadata after trajectory is complete
            flight_summary = flight.get_flight_summary()
            if self.exporter:
                self.exporter.export_flight_metadata_to_postgres(flight_summary)

def create_grafana_dashboard_config() -> Dict:
    """Generate Grafana dashboard configuration JSON"""
    return {
        "dashboard": {
            "id": None,
            "title": "ADS-B Flight Trajectories",
            "tags": ["adsb", "aviation", "trajectories"],
            "timezone": "browser",
            "panels": [
                {
                    "id": 1,
                    "title": "Flight Trajectories Map",
                    "type": "geomap",
                    "targets": [
                        {
                            "datasource": "InfluxDB",
                            "query": 'from(bucket: "adsb-trajectories") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "trajectory")'
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "custom": {
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                }
                            }
                        }
                    },
                    "options": {
                        "view": {
                            "id": "coords",
                            "lat": 48.8566,
                            "lon": 2.3522,
                            "zoom": 10
                        },
                        "controls": {
                            "mouseWheelZoom": True,
                            "showZoom": True,
                            "showAttribution": True
                        },
                        "basemap": {
                            "type": "default"
                        }
                    }
                },
                {
                    "id": 2,
                    "title": "Altitude Profiles",
                    "type": "timeseries",
                    "targets": [
                        {
                            "datasource": "InfluxDB",
                            "query": 'from(bucket: "adsb-trajectories") |> range(start: -1h) |> filter(fn: (r) => r._field == "altitude")'
                        }
                    ]
                },
                {
                    "id": 3,
                    "title": "Flight Statistics",
                    "type": "stat",
                    "targets": [
                        {
                            "datasource": "PostgreSQL",
                            "query": "SELECT COUNT(*) as total_flights, SUM(CASE WHEN is_landing THEN 1 ELSE 0 END) as landings, SUM(CASE WHEN is_takeoff THEN 1 ELSE 0 END) as takeoffs FROM flight_metadata WHERE start_time > NOW() - INTERVAL '1 hour'"
                        }
                    ]
                }
            ],
            "time": {
                "from": "now-1h",
                "to": "now"
            },
            "refresh": "5s"
        }
    }

def setup_grafana_databases():
    """Setup database schemas for Grafana integration"""
    print("Setting up Grafana databases...")
    
    # PostgreSQL schema
    if POSTGRESQL_AVAILABLE:
        try:
            engine = create_engine(f"postgresql://{GRAFANA_CONFIG['postgresql']['user']}:{GRAFANA_CONFIG['postgresql']['password']}@{GRAFANA_CONFIG['postgresql']['host']}:{GRAFANA_CONFIG['postgresql']['port']}/{GRAFANA_CONFIG['postgresql']['database']}")
            
            schema_sql = """
            CREATE TABLE IF NOT EXISTS flight_metadata (
                flight_id VARCHAR(100) PRIMARY KEY,
                icao24 VARCHAR(10),
                callsign VARCHAR(20),
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_minutes FLOAT,
                total_points INTEGER,
                altitude_min FLOAT,
                altitude_max FLOAT,
                vertical_rate_min FLOAT,
                vertical_rate_max FLOAT,
                is_landing BOOLEAN,
                is_takeoff BOOLEAN,
                start_lat FLOAT,
                start_lon FLOAT,
                end_lat FLOAT,
                end_lon FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_flight_start_time ON flight_metadata(start_time);
            CREATE INDEX IF NOT EXISTS idx_flight_icao24 ON flight_metadata(icao24);
            CREATE INDEX IF NOT EXISTS idx_flight_callsign ON flight_metadata(callsign);
            """
            
            with engine.connect() as conn:
                conn.execute(schema_sql)
                conn.commit()
            
            print("PostgreSQL schema created successfully")
            
        except Exception as e:
            print(f"Error setting up PostgreSQL: {e}")
    
    # InfluxDB bucket creation would be done through InfluxDB UI or CLI
    print("InfluxDB bucket 'adsb-trajectories' should be created manually")

def check_data_file_exists():
    """Search for ADS-B data files in multiple locations and return correct path"""
    possible_paths = [
        "adsb25/orly.jsonl.gz",
        "TP_FINAL/adsb25/orly.jsonl.gz", 
        "../TP_FINAL/adsb25/orly.jsonl.gz",
        "./adsb25/orly.jsonl.gz"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError(f"ADS-B data file not found. Searched paths: {possible_paths}")

# %%
# Example usage and testing
if __name__ == "__main__":
    print("ADS-B Grafana Integration Test")
    print("=" * 50)
    
    # Initialize Grafana exporter
    exporter = GrafanaExporter()
    
    # Load data (using existing file structure)
    print("\nLoading ADS-B data...")
    try:
        data_file_path = check_data_file_exists()
        flight_collection = FlightCollectionGrafana.read_jsonl_gz(
            data_file_path, 
            exporter
        )
        print(f"Loaded collection with {len(flight_collection)} flights")
        
        # Get statistics
        stats = flight_collection.get_statistics()
        print(f"Statistics: {stats}")
        
        # Filter flights
        landings = flight_collection.filter_landings()
        takeoffs = flight_collection.filter_takeoffs()
        
        print(f"Found {len(landings)} landings and {len(takeoffs)} takeoffs")
        
        # Export sample flights to Grafana (limit for testing)
        if landings or takeoffs:
            print("\nExporting sample flights to Grafana...")
            sample_flights = (landings[:2] + takeoffs[:2])  # Export 4 sample flights
            
            for flight in sample_flights:
                print(f"Processing flight: {flight.flight_id}")
                summary = flight.get_flight_summary()
                print(f"  Duration: {summary['duration_minutes']:.1f} minutes")
                print(f"  Points: {summary['total_points']}")
                print(f"  Altitude range: {summary['altitude_min']}-{summary['altitude_max']} ft")
                
                # Uncomment to actually export (requires database setup)
                # flight.export_to_grafana()
        
        # Generate dashboard configuration
        dashboard_config = create_grafana_dashboard_config()
        
        # Save dashboard config to file
        with open("grafana_dashboard_config.json", "w") as f:
            json.dump(dashboard_config, f, indent=2)
        
        print("\nGrafana dashboard configuration saved to 'grafana_dashboard_config.json'")
        print("Setup complete! See documentation for database configuration.")
        
    except FileNotFoundError as e:
        print(f"ADS-B data file not found: {e}")
        print("Please ensure the data file exists in one of the expected locations:")
        print("- adsb25/orly.jsonl.gz")
        print("- TP_FINAL/adsb25/orly.jsonl.gz") 
        print("- ../TP_FINAL/adsb25/orly.jsonl.gz")
        print("- ./adsb25/orly.jsonl.gz")
    except Exception as e:
        print(f"Error during processing: {e}")

# %%
# Additional utility functions for Grafana integration

def export_sample_data_csv():
    """Export sample data to CSV for manual Grafana testing"""
    print("Exporting sample data to CSV...")
    
    try:
        data_file_path = check_data_file_exists()
        flight_collection = FlightCollectionGrafana.read_jsonl_gz(data_file_path)
        landings = flight_collection.filter_landings()
        
        if landings:
            print(f"Found {len(landings)} landing trajectories")
            
            # Collect all trajectories
            all_trajectories = []
            
            for flight in landings:
                trajectory = flight.get_trajectory()
                
                # Prepare data for Grafana CSV import - select available columns
                base_columns = ['timestamp_dt', 'latitude', 'longitude', 'altitude', 'vertical_rate']
                available_columns = [col for col in base_columns if col in trajectory.columns]
                
                # Add ground_speed if available
                if 'ground_speed' in trajectory.columns:
                    available_columns.append('ground_speed')
                
                csv_data = trajectory[available_columns].copy()
                csv_data['flight_id'] = flight.flight_id
                csv_data['icao24'] = flight.icao24
                csv_data['callsign'] = flight.callsign
                
                all_trajectories.append(csv_data)
            
            # Combine all trajectories
            combined_data = pd.concat(all_trajectories, ignore_index=True)
            
            # Round timestamps to seconds (remove nanoseconds for Grafana compatibility)
            combined_data['timestamp_dt'] = pd.to_datetime(combined_data['timestamp_dt']).dt.floor('S')
            
            combined_data.to_csv('sample_trajectory_for_grafana.csv', index=False)
            print(f"All {len(landings)} trajectories exported to 'sample_trajectory_for_grafana.csv'")
            print(f"Total data points: {len(combined_data)}")
            
    except Exception as e:
        print(f"Error exporting CSV: {e}")

def export_takeoffs_csv():
    """Export takeoff trajectories to CSV for manual Grafana testing"""
    print("Exporting takeoff trajectories to CSV...")
    
    try:
        data_file_path = check_data_file_exists()
        flight_collection = FlightCollectionGrafana.read_jsonl_gz(data_file_path)
        takeoffs = flight_collection.filter_takeoffs()
        
        if takeoffs:
            print(f"Found {len(takeoffs)} takeoff trajectories")
            
            # Collect all trajectories
            all_trajectories = []
            
            for flight in takeoffs:
                trajectory = flight.get_trajectory()
                
                # Prepare data for Grafana CSV import - select available columns
                base_columns = ['timestamp_dt', 'latitude', 'longitude', 'altitude', 'vertical_rate']
                available_columns = [col for col in base_columns if col in trajectory.columns]
                
                # Add ground_speed if available
                if 'ground_speed' in trajectory.columns:
                    available_columns.append('ground_speed')
                
                csv_data = trajectory[available_columns].copy()
                csv_data['flight_id'] = flight.flight_id
                csv_data['icao24'] = flight.icao24
                csv_data['callsign'] = flight.callsign
                
                all_trajectories.append(csv_data)
            
            # Combine all trajectories
            combined_data = pd.concat(all_trajectories, ignore_index=True)
            
            # Round timestamps to seconds (remove nanoseconds for Grafana compatibility)
            combined_data['timestamp_dt'] = pd.to_datetime(combined_data['timestamp_dt']).dt.floor('s')
            
            combined_data.to_csv('takeoffs_trajectory_for_grafana.csv', index=False)
            print(f"All {len(takeoffs)} takeoff trajectories exported to 'takeoffs_trajectory_for_grafana.csv'")
            print(f"Total data points: {len(combined_data)}")
            
    except Exception as e:
        print(f"Error exporting takeoffs CSV: {e}")

def generate_requirements_txt():
    """Generate requirements.txt for Grafana integration"""
    requirements = [
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "geopandas>=0.10.0",
        "matplotlib>=3.5.0",
        "pyproj>=3.2.0",
        "shapely>=1.8.0",
        "influxdb-client>=1.24.0",
        "psycopg2-binary>=2.9.0",
        "sqlalchemy>=1.4.0"
    ]
    
    with open("requirements_grafana.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("Requirements file saved to 'requirements_grafana.txt'")

# Run utility functions
if __name__ == "__main__":
    export_sample_data_csv()
    generate_requirements_txt()
