# 🚕 Bangkok Taxi Analysis - City Planner Insights

> **Author:** Chana  
> **Branch:** ChanaCityPlaner  
> **Purpose:** Analyzing Bangkok taxi GPS data to identify city planning opportunities

## 📋 Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Analysis Features](#analysis-features)
- [Output Files](#output-files)
- [Visualization](#visualization)
- [Data Dictionary](#data-dictionary)

---

## 🎯 Overview

This project analyzes **55+ million GPS records** from Bangkok taxis to provide actionable insights for city planners. The analysis focuses on three key areas:

1. **🌃 Nighttime Economic Zones** - Identifying high-demand areas during night hours
2. **🚕 Taxi Deserts** - Finding service gaps where taxis are underutilized
3. **🌅🌙 Day vs Night Patterns** - Comparing activity patterns across time periods

### Key Statistics
- **Total Records:** 55,483,806 GPS points
- **Time Periods:** DAY (06:00-17:59), NIGHT (18:00-05:59)
- **Coverage:** Bangkok Metropolitan Region
- **Spatial Resolution:** ~100m grid cells

---

## 🛠️ Requirements

### Software
- Python 3.13+
- Apache PySpark 4.0.1
- PyArrow 22.0.0
- Folium (for visualization)
- Pandas

### Installation
```bash
# Install Python dependencies
pip3 install pyspark pyarrow folium pandas

# Verify PySpark installation
spark-submit --version
```

---

## 🚀 Quick Start

### 1. Run the Main Analysis
```bash
# Execute PySpark analysis (generates all output files)
spark-submit analysis_day_night.py
```

**Processing time:** ~5-10 minutes on local machine

### 2. Generate Visualizations
```bash
# Option A: Night demand zones + taxi deserts
python3 create_maps.py

# Option B: Day vs Night comparison
python3 create_day_night_comparison.py
```

### 3. View Results
```bash
# Open interactive maps in browser
open map1_night_demand.html
open map2_taxi_deserts.html
open map_day_night_comparison.html
```

---

## 📊 Analysis Features

### 1. Day/Night Activity Analysis
- **File:** `analysis_day_night.py`
- **Output:** `output_day_night_activity/`
- **Purpose:** Spatial clustering of taxi activity by time period

**Time Period Definitions:**
- **DAY:** 06:00 - 17:59 (daytime hours)
- **NIGHT:** 18:00 - 05:59 (nighttime hours)

### 2. Night Demand Zones
- **Output:** `output_night_demand_zones/`
- **Time Range:** 18:00 - 05:59
- **Metrics:** 
  - Occupied taxi count
  - Available taxi count
  - Demand-to-supply ratio
- **Purpose:** Identify high-demand areas during nighttime hours

### 3. Taxi Deserts Detection
- **Output:** `output_taxi_deserts/`
- **Time Range:** 22:00 - 04:00 (late night subset)
- **Definition:** Areas with >50% unhired taxis
- **Insight:** Indicates service inefficiency and repositioning opportunities

### 4. Day vs Night Comparison
- **Script:** `create_day_night_comparison.py`
- **Time Periods:** DAY (06:00-17:59) vs NIGHT (18:00-05:59)
- **Purpose:** Compare activity patterns across daytime and nighttime
- **Note:** Results will differ from old analysis due to new time definitions

---

## 📁 Output Files

### Analysis Outputs
```
output_day_night_activity/     # 232MB - All spatial-temporal activity
output_night_demand_zones/     # 20KB - High-demand night zones
output_taxi_deserts/           # 1KB - Service gap zones
output_trip_comparison/        # Empty (data limitation)
```

### Visualization Outputs
```
map1_night_demand.html         # Night demand zones (red/orange circles)
map2_taxi_deserts.html         # Taxi deserts (purple circles)
map3_combined.html             # Combined view with layer control
map_day_night_comparison.html  # Day vs night activity comparison
```

---

## 🗺️ Visualization

### Interactive Map Features
All maps are built with **Folium** and include:
- ✅ Click circles for detailed popup info
- ✅ Zoom/pan navigation
- ✅ Layer toggle controls
- ✅ Color-coded by intensity
- ✅ Size-coded by activity volume

### Map Legend

| Map | Color | Meaning |
|-----|-------|---------|
| Night Demand | 🔴 Red | Extreme demand (ratio > 100) |
| Night Demand | 🟠 Orange | High demand |
| Taxi Deserts | 🟣 Purple | High % unhired taxis |
| Day Activity | 🔵 Blue | Daytime zones (06:00-17:59) |
| Day-Only | 🟢 Green | Active only during day |
| Night-Only | 🟣 Purple | Active only at night (18:00-05:59) |

### Running Jupyter Notebook (Optional)
```bash
# If you have Python extension installed in VS Code:
# 1. Open visualize_taxi_maps.ipynb
# 2. Select Python 3.13 kernel
# 3. Click "Run All"
```

---

## 🏙️ City Planner Applications

### 1. Economic Zone Planning
- Identify nighttime economic hubs for infrastructure investment
- Optimize street lighting and security in high-activity zones
- Plan taxi stand locations in demand hotspots

### 2. Service Gap Analysis
- Redirect taxis from desert zones to demand zones
- Optimize taxi dispatch algorithms
- Reduce empty taxi cruising time

### 3. Functional Zone Shift
- Understand how areas transform between day/night
- Plan mixed-use developments
- Optimize public transport schedules

---

## 📖 Data Dictionary

### Processed Data Schema
**File:** `processed_taxi_data_fixed.parquet` (560MB)

**Note:** Original data had column corruption. Fixed using `fix_parquet.py`


| Column Name                    | Type      | Description                                                                                                             |
| ------------------------------ | --------- | ----------------------------------------------------------------------------------------------------------------------- |
| vehicle_id                     | integer   | Sequential ID (0-55M) - NOTE: Not real vehicle tracking due to data corruption                                          |
| date_only                      | date      | Date of the record (YYYY-MM-DD)                                                                                         |
| timestamp                      | timestamp | Exact timestamp of the record (milliseconds since epoch)                                                                |
| lat                            | double    | Latitude coordinate of the taxi (Bangkok area: ~13.5-14.0)                                                              |
| lon                            | double    | Longitude coordinate of the taxi (Bangkok area: ~100.3-100.8)                                                           |
| speed                          | double    | Vehicle speed (km/h)                                                                                                    |
| heading                        | integer   | Direction of travel in degrees (0-359)                                                                                  |
| for_hire_light                 | integer   | 1 if taxi is available for hire, 0 if occupied                                                                          |
| engine_acc                     | integer   | 1 if engine is on, 0 if off                                                                                             |
| gpsvalid                       | integer   | 1 if GPS signal is valid, 0 otherwise                                                                                   |
| hour                           | integer   | Hour of the day (0-23)                                                                                                  |

### Analysis-Generated Fields

| Column Name     | Type   | Description                                               |
|-----------------|--------|-----------------------------------------------------------|
| lat_bin         | double | Rounded latitude (3 decimals) - creates ~100m grid cells  |
| lon_bin         | double | Rounded longitude (3 decimals) - creates ~100m grid cells |
| time_period     | string | DAY, NIGHT, or OTHER based on hour                        |
| occupied_count  | int    | Number of occupied taxis in zone                          |
| available_count | int    | Number of available taxis in zone                         |
| unhired_count   | int    | Number of unhired taxis (taxi deserts analysis)           |
| demand_supply_ratio | double | Ratio of occupied to available taxis                   |
| desert_score    | double | Percentage of unhired taxis in zone (0.0-1.0)             |

---

## 🔧 Troubleshooting

### Issue: Python Extension Not Installed
**Error:** "Failed to install the Python Extension"  
**Solution:** Use Python scripts instead of Jupyter notebooks
```bash
python3 create_maps.py
```

### Issue: PySpark Memory Error
**Solution:** Reduce data processing by filtering to smaller area
```python
# In analysis_day_night.py, add early filter:
df = df.filter((col('lat') > 13.6) & (col('lat') < 13.9))
```

### Issue: Empty Output Files
**Cause:** Sequential vehicle_id prevents trip tracking  
**Status:** Expected - use spatial analysis instead of trip-based analysis

---

## 📝 Project Structure

```
taxi_data_analysis/
├── README.md                          # This file
├── analysis_day_night.py              # Main PySpark analysis script
├── fix_parquet.py                     # Data corruption fix script
├── create_maps.py                     # Night demand + deserts visualization
├── create_day_night_comparison.py     # Day vs night comparison map
├── view_results_simple.py             # Terminal-based results viewer
├── city_planner_report.py             # Comprehensive text report
├── visualize_taxi_maps.ipynb          # Jupyter notebook (optional)
├── processed_taxi_data_fixed.parquet  # Fixed data file (560MB)
├── output_day_night_activity/         # Analysis output (232MB)
├── output_night_demand_zones/         # Night demand zones (20KB)
├── output_taxi_deserts/               # Taxi desert zones (1KB)
└── *.html                             # Interactive map outputs
```

---

## 🤝 Team Collaboration

### Before You Start
1. **Read this README completely**
2. **Check you're on the correct branch:** `ChanaCityPlaner`
3. **Install all dependencies** (see Requirements section)
4. **Run the Quick Start** to verify everything works

### Working with the Code

**Don't modify these files (analysis outputs):**
- `output_*/` directories
- `processed_taxi_data_fixed.parquet`
- `*.html` map files

**Safe to modify:**
- Visualization scripts (`create_*.py`)
- Analysis parameters in `analysis_day_night.py`
- This README

### Running Analysis from Scratch
```bash
# 1. Fix data (only if you have original corrupted parquet)
python3 fix_parquet.py

# 2. Run analysis
spark-submit analysis_day_night.py

# 3. Generate visualizations
python3 create_maps.py
python3 create_day_night_comparison.py

# 4. View results
open map_day_night_comparison.html
```

---

## 📊 Key Insights Summary

### Nighttime Economic Zones (18:00-05:59)
- High-demand zones identified during nighttime hours
- Includes evening commute, nightlife, and early morning activity
- **Analysis:** Occupied vs available taxi ratio by location

### Taxi Deserts (22:00-04:00)
- **26 desert zones** with >50% unhired rate
- **Indicates:** Service inefficiency, repositioning needed
- **Opportunity:** Optimize taxi dispatch to demand zones

### Day vs Night Activity
- **Daytime (06:00-17:59):** All daylight and business hours
- **Nighttime (18:00-05:59):** Evening, night, and early morning hours
- **Note:** New time definitions provide more comprehensive coverage
- Results will show different patterns compared to previous narrow time windows

---

## 📞 Contact & Questions

**Branch Owner:** Chana  
**Branch:** ChanaCityPlaner  
**Project:** Senior Project - Bangkok Taxi Analysis

For questions about:
- **Analysis methodology** → Check `analysis_day_night.py` comments
- **Data issues** → See fix_parquet.py and Troubleshooting section
- **Visualization** → Modify `create_*.py` scripts
- **City planning insights** → Run `python3 city_planner_report.py`

---

## 📚 References

- **PySpark Documentation:** https://spark.apache.org/docs/latest/api/python/
- **Folium Documentation:** https://python-visualization.github.io/folium/
- **Original Data Source:** Bangkok taxi GPS dataset

---

**Last Updated:** November 24, 2025  
**Version:** 1.0  
**Status:** ✅ Analysis Complete, Ready for Review

| is_tourist_activity_proxy      | integer   | 1 if likely tourist activity (location, time, not rush hour, hired), 0 otherwise                                        |
| is_airport_fare_area           | integer   | 1 if hired and very close to airport, 0 otherwise                                                                       |
| time_diff_seconds              | long      | Time difference from previous record (seconds)                                                                          |
| distance_traveled_km           | double    | Distance traveled since previous record (km)                                                                            |
| calculated_speed_kmh           | double    | Speed calculated from distance/time (km/h)                                                                              |
| trip_start                     | integer   | 1 if trip started at this record, 0 otherwise                                                                           |
| trip_end                       | integer   | 1 if trip ended at this record, 0 otherwise                                                                             |
| cardinal_direction             | string    | Cardinal direction (N, NE, E, SE, S, SW, W, NW)                                                                         |
| stop_duration                  | long      | Duration of stop (seconds)                                                                                              |
| is_long_stop                   | integer   | 1 if stop duration > 5 minutes, 0 otherwise                                                                             |
| data_quality_flag              | string    | Data quality: normal or irregular                                                                                       |
| speed_validation_flag          | string    | Speed validation: ok or mismatch                                                                                        |
| daily_ping_count               | long      | Number of records for the vehicle on that day                                                                           |
| daily_avg_speed                | double    | Average speed for the vehicle on that day                                                                               |
| daily_max_speed                | double    | Maximum speed for the vehicle on that day                                                                               |
| daily_total_distance_km        | double    | Total distance traveled by the vehicle on that day                                                                      |
| daily_hired_pings              | long      | Number of records where taxi was hired on that day                                                                      |
| daily_searching_fare_pings     | long      | Number of records searching for fare on that day                                                                        |
| daily_idle_pings               | long      | Number of records idle on that day                                                                                      |
| daily_stationary_pings         | long      | Number of records stationary on that day                                                                                |
| daily_moving_pings             | long      | Number of records moving on that day                                                                                    |
| daily_trip_starts              | long      | Number of trip starts on that day                                                                                       |
| daily_trip_ends                | long      | Number of trip ends on that day                                                                                         |
| daily_day_shift_pings          | long      | Number of records during day shift on that day                                                                          |
| daily_night_shift_pings        | long      | Number of records during night shift on that day                                                                        |
| daily_bmr_pings                | long      | Number of records within BMR on that day                                                                                |
| daily_utilization_rate         | double    | Fraction of time taxi was hired (hired pings / total pings)                                                             |
| daily_empty_rate               | double    | Fraction of time taxi was searching for fare while moving                                                               |
| daily_night_ratio              | double    | Fraction of records during night shift                                                                                  |
| year                           | integer   | Year of the record                                                                                                      |
| month                          | integer   | Month of the record                                                                                                     |

## Notes

- All fields may contain null values if data is missing or not applicable.
- This data is processed and aggregated from raw taxi GPS records.
- For more details on data processing, see the relevant notebooks in this project.
