# ADS-B Trajectory Visualization with Grafana

This guide explains how to set up Grafana to visualize ADS-B aircraft trajectories using the enhanced `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py` implementation.

## Architecture Overview

```
ADS-B JSON Data → ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py → InfluxDB (time-series) + PostgreSQL (metadata) → Grafana Dashboard
```

### Components:
- **InfluxDB**: Stores trajectory points as time-series data
- **PostgreSQL**: Stores flight metadata and statistics
- **Grafana**: Visualizes data with maps, charts, and dashboards
- **ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py**: Enhanced Flight classes with export capabilities

## Prerequisites

### 1. Install Required Python Packages

```bash
pip install -r requirements_grafana.txt
```

Or install individually:
```bash
pip install pandas numpy geopandas matplotlib pyproj shapely
pip install influxdb-client psycopg2-binary sqlalchemy
```

### 2. Install and Configure InfluxDB

#### Option A: Docker (Recommended)
```bash
# Pull and run InfluxDB
docker run -d -p 8086:8086 \
  -v influxdb-storage:/var/lib/influxdb2 \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=password123 \
  -e DOCKER_INFLUXDB_INIT_ORG=adsb-org \
  -e DOCKER_INFLUXDB_INIT_BUCKET=adsb-trajectories \
  influxdb:2.7
```

#### Option B: Local Installation
1. Download from [InfluxDB Downloads](https://portal.influxdata.com/downloads/)
2. Install and start the service
3. Access web UI at `http://localhost:8086`
4. Create organization: `adsb-org`
5. Create bucket: `adsb-trajectories`
6. Generate API token with write permissions

### 3. Install and Configure PostgreSQL

#### Option A: Docker
```bash
# Run PostgreSQL with PostGIS extension
docker run -d -p 5432:5432 \
  -e POSTGRES_DB=adsb_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password123 \
  -v postgres-data:/var/lib/postgresql/data \
  postgis/postgis:15-3.3
```

#### Option B: Local Installation
1. Install PostgreSQL from [official site](https://www.postgresql.org/download/)
2. Create database: `adsb_db`
3. Install PostGIS extension (optional, for advanced geospatial queries)

### 4. Install and Configure Grafana

#### Option A: Docker
```bash
# Run Grafana
docker run -d -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

#### Option B: Local Installation
1. Download from [Grafana Downloads](https://grafana.com/grafana/download)
2. Install and start service
3. Access web UI at `http://localhost:3000` (admin/admin)

## Configuration

### 1. Update Configuration in ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py

Edit the `GRAFANA_CONFIG` dictionary:

```python
GRAFANA_CONFIG = {
    'influxdb': {
        'url': 'http://localhost:8086',
        'token': 'your-influxdb-api-token',  # Get from InfluxDB UI
        'org': 'adsb-org',
        'bucket': 'adsb-trajectories'
    },
    'postgresql': {
        'host': 'localhost',
        'port': 5432,
        'database': 'adsb_db',
        'user': 'postgres',
        'password': 'password123'
    }
}
```

### 2. Setup Database Schemas

Run the setup function in Python:

```python
from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import setup_grafana_databases
setup_grafana_databases()
```

### 3. Configure Grafana Data Sources

#### InfluxDB Data Source:
1. Go to Grafana → Configuration → Data Sources
2. Add InfluxDB data source
3. Configure:
   - **URL**: `http://localhost:8086`
   - **Organization**: `adsb-org`
   - **Token**: Your InfluxDB API token
   - **Default Bucket**: `adsb-trajectories`

#### PostgreSQL Data Source:
1. Add PostgreSQL data source
2. Configure:
   - **Host**: `localhost:5432`
   - **Database**: `adsb_db`
   - **User**: `postgres`
   - **Password**: `password123`

## Usage

### 1. Basic Data Export

```python
from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import FlightCollectionGrafana, GrafanaExporter

# Initialize exporter
exporter = GrafanaExporter()

# Load ADS-B data
flight_collection = FlightCollectionGrafana.read_jsonl_gz(
    "adsb25/orly.jsonl.gz", 
    exporter
)

# Export all flights (limit for testing)
results = flight_collection.export_all_to_grafana(max_flights=10)
print(f"Exported {results['exported']} flights")
```

### 2. Real-time Streaming Simulation

```python
# Stream data to simulate real-time updates
flight_collection.stream_to_grafana(interval_seconds=5)
```

### 3. Export Individual Flight

```python
# Get specific flight
landings = flight_collection.filter_landings()
if landings:
    flight = landings[0]
    success = flight.export_to_grafana()
    print(f"Export successful: {success}")
```

## Grafana Dashboard Setup

### 1. Import Dashboard Configuration

The script generates `grafana_dashboard_config.json`. Import this in Grafana:

1. Go to Dashboards → Import
2. Upload the JSON file
3. Configure data sources if needed

### 2. Manual Panel Creation

#### Flight Trajectories Map Panel:
- **Type**: Geomap
- **Data Source**: InfluxDB
- **Query**: 
  ```flux
  from(bucket: "adsb-trajectories")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "trajectory")
    |> filter(fn: (r) => r._field == "latitude" or r._field == "longitude")
  ```

#### Altitude Profile Panel:
- **Type**: Time Series
- **Data Source**: InfluxDB
- **Query**:
  ```flux
  from(bucket: "adsb-trajectories")
    |> range(start: -1h)
    |> filter(fn: (r) => r._field == "altitude")
  ```

#### Flight Statistics Panel:
- **Type**: Stat
- **Data Source**: PostgreSQL
- **Query**:
  ```sql
  SELECT 
    COUNT(*) as total_flights,
    SUM(CASE WHEN is_landing THEN 1 ELSE 0 END) as landings,
    SUM(CASE WHEN is_takeoff THEN 1 ELSE 0 END) as takeoffs
  FROM flight_metadata 
  WHERE start_time > NOW() - INTERVAL '1 hour'
  ```

## Advanced Features

### 1. Geospatial Queries

For advanced mapping, install Grafana plugins:
```bash
# Install Grafana plugins
grafana-cli plugins install grafana-worldmap-panel
grafana-cli plugins install grafana-trackmap-panel
```

### 2. Custom Alerts

Set up alerts for:
- Unusual flight patterns
- Emergency altitude changes
- High traffic periods

### 3. Data Retention

Configure data retention policies:

#### InfluxDB:
```flux
// Retain trajectory data for 30 days
option task = {name: "retention-policy", every: 1h}

from(bucket: "adsb-trajectories")
  |> range(start: -30d)
  |> drop()
```

#### PostgreSQL:
```sql
-- Clean old metadata (older than 90 days)
DELETE FROM flight_metadata 
WHERE start_time < NOW() - INTERVAL '90 days';
```

## Troubleshooting

### Common Issues:

1. **Connection Errors**:
   - Check database services are running
   - Verify connection parameters
   - Check firewall settings

2. **Data Not Appearing**:
   - Verify time ranges in Grafana
   - Check data source configurations
   - Ensure data is being exported correctly

3. **Performance Issues**:
   - Add database indexes
   - Limit query time ranges
   - Use data sampling for large datasets

### Debug Commands:

```python
# Test database connections
from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import GrafanaExporter
exporter = GrafanaExporter()

# Check InfluxDB connection
if exporter.influx_client:
    print("InfluxDB connected")

# Check PostgreSQL connection
if exporter.postgres_engine:
    print("PostgreSQL connected")
```

## Sample Queries

### InfluxDB Flux Queries:

```flux
// All trajectories in last hour
from(bucket: "adsb-trajectories")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "trajectory")

// Specific aircraft
from(bucket: "adsb-trajectories")
  |> range(start: -24h)
  |> filter(fn: (r) => r.icao24 == "ABC123")

// High altitude flights
from(bucket: "adsb-trajectories")
  |> range(start: -1h)
  |> filter(fn: (r) => r._field == "altitude")
  |> filter(fn: (r) => r._value > 30000)
```

### PostgreSQL Queries:

```sql
-- Recent landings
SELECT * FROM flight_metadata 
WHERE is_landing = true 
AND start_time > NOW() - INTERVAL '1 hour'
ORDER BY start_time DESC;

-- Flight statistics by hour
SELECT 
  DATE_TRUNC('hour', start_time) as hour,
  COUNT(*) as total_flights,
  AVG(duration_minutes) as avg_duration
FROM flight_metadata 
WHERE start_time > NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour;
```

## Next Steps

1. **Customize Dashboards**: Create specific views for your use case
2. **Add Alerts**: Set up notifications for interesting events
3. **Integrate APIs**: Connect to live ADS-B feeds for real-time data
4. **Scale Up**: Use clustering for high-volume data processing

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Grafana documentation
3. Check database logs
4. Test with sample data first

---

**Note**: This setup is designed for development and testing. For production use, implement proper security, authentication, and monitoring.
