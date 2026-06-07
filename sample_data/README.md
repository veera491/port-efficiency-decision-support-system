# Sample Data Directory

To run this Decision Support System locally, you need a compatible Automatic Identification System (AIS) dataset.

The original dataset used for the academic case study contains 1,330,169 records and 25 columns, focused on the Baltic Sea / German Port region. For privacy and size constraints, it is excluded from this public repository.

## Dataset Structure
If you wish to test the system with your own data, ensure your CSV file (e.g., `PRJ912.csv` or directly as `PreProcessedData.csv`) contains the following key columns utilized by the preprocessing and analytics scripts:

* `MMSI` (Maritime Mobile Service Identity)
* `TimePosition` (Timestamp of position)
* `TimeETA` (Estimated Time of Arrival)
* `TimeVoyage` (Voyage start/timestamp)
* `Latitude`
* `Longitude`
* `Name` (Vessel Name)
* `VesselType`
* `Speed`
* `NavStatus` (Navigation Status)
* `Length`
* `Width`
* `SourcePosition`
* `Destination`

Place your `PreProcessedData.csv` in the root directory (or update the path in `src/app.py` accordingly) before running the Flask server.
