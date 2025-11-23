# Taxi Processed Data Dictionary

This README describes the schema of the processed taxi data stored in `output/taxi_processed.parquet`.

## Data Fields

| Column Name                    | Type      | Description                                                                                                             |
| ------------------------------ | --------- | ----------------------------------------------------------------------------------------------------------------------- |
| vehicle_id                     | string    | Unique identifier for each taxi vehicle                                                                                 |
| date_only                      | date      | Date of the record (YYYY-MM-DD)                                                                                         |
| timestamp                      | timestamp | Exact timestamp of the record (Bangkok time)                                                                            |
| lat                            | double    | Latitude coordinate of the taxi                                                                                         |
| lon                            | double    | Longitude coordinate of the taxi                                                                                        |
| speed                          | double    | Vehicle speed (km/h)                                                                                                    |
| heading                        | integer   | Direction of travel in degrees (0-359)                                                                                  |
| for_hire_light                 | integer   | 1 if taxi is available for hire, 0 if occupied                                                                          |
| engine_acc                     | integer   | 1 if engine is on, 0 if off                                                                                             |
| gpsvalid                       | integer   | 1 if GPS signal is valid, 0 otherwise                                                                                   |
| hour                           | integer   | Hour of the day (0-23)                                                                                                  |
| day_of_week                    | integer   | Day of week (0=Sunday, 6=Saturday)                                                                                      |
| day_name                       | string    | Name of the day (e.g., Monday)                                                                                          |
| is_weekend                     | integer   | 1 if record is on a weekend, 0 otherwise                                                                                |
| time_of_day                    | string    | Time period: morning, afternoon, evening, night                                                                         |
| day_night_shift                | string    | Shift type: day_shift or night_shift                                                                                    |
| is_rush_hour                   | integer   | 1 if during rush hour, 0 otherwise                                                                                      |
| is_hired                       | integer   | 1 if taxi is hired/occupied, 0 otherwise                                                                                |
| is_searching_fare              | integer   | 1 if taxi is vacant and moving, 0 otherwise                                                                             |
| is_idle                        | integer   | 1 if engine is off, 0 otherwise                                                                                         |
| is_moving                      | integer   | 1 if speed > 3 km/h, 0 otherwise                                                                                        |
| is_stationary                  | integer   | 1 if speed <= 3 km/h, 0 otherwise                                                                                       |
| speed_category                 | string    | Speed group: stationary, slow, moderate, fast, very_fast                                                                |
| distance_from_bangkok_km       | double    | Distance from Bangkok center (km)                                                                                       |
| distance_from_nakhon_pathom_km | double    | Distance from Nakhon Pathom center (km)                                                                                 |
| distance_from_pathum_thani_km  | double    | Distance from Pathum Thani center (km)                                                                                  |
| distance_from_nonthaburi_km    | double    | Distance from Nonthaburi center (km)                                                                                    |
| distance_from_samut_prakan_km  | double    | Distance from Samut Prakan center (km)                                                                                  |
| distance_from_samut_sakhon_km  | double    | Distance from Samut Sakhon center (km)                                                                                  |
| is_in_bmr                      | integer   | 1 if within Bangkok Metropolitan Region, 0 otherwise                                                                    |
| lat_grid                       | double    | Latitude grid cell (rounded, ~1.1km)                                                                                    |
| lon_grid                       | double    | Longitude grid cell (rounded, ~1.1km)                                                                                   |
| distance_to_nearest_center_km  | double    | Distance to the nearest province center (km)                                                                            |
| nearest_province               | string    | Name of the nearest province center                                                                                     |
| area_type                      | string    | Area classification: bangkok_center_core, bangkok_inner_ring, bangkok_outer_belt, bmr_suburban_area, outside_bmr_region |
| grid_cell                      | string    | Combined lat/lon grid cell identifier                                                                                   |
| distance_to_bkk_airport_km     | double    | Distance to Suvarnabhumi Airport (km)                                                                                   |
| distance_to_dmk_airport_km     | double    | Distance to Don Mueang Airport (km)                                                                                     |
| distance_to_grand_palace_km    | double    | Distance to Grand Palace (km)                                                                                           |
| distance_to_chatuchak_km       | double    | Distance to Chatuchak Market (km)                                                                                       |
| is_near_tourist_hub            | integer   | 1 if near a major tourist hub, 0 otherwise                                                                              |
| is_tourist_time                | integer   | 1 if during typical tourist hours, 0 otherwise                                                                          |
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
