# Port Efficiency Decision Support System

An academic Decision Support System (DSS) prototype designed for analyzing port efficiency and maritime logistics, focusing on a Baltic Sea / German port case study context.

## 📌 Project Context
This repository contains the source code for an academic prototype analyzing vessel movements and port efficiency. The system processes AIS (Automatic Identification System) data to compute and visualize critical operational metrics, offering insights into maritime logistics.

* **Domain:** German Port Authority / Baltic Sea Maritime Logistics.
* **Scope:** Academic Decision Support System prototype.
* **Dataset Context:** Evaluated on 1,330,169 AIS records (25 dimensions/columns).
* **Credit:** Core implementation and modeling by Veerababu Sutapalli.

> **Note:** For privacy and repository size constraints, the raw 1.3M record dataset (`PRJ912.csv`) and the large preprocessed dataset are excluded from this repository. Please see the `sample_data/README.md` for instructions on how to use your own data.

## 🏗 System Architecture
* **Backend Framework:** Python Flask
* **Data Processing:** pandas, NumPy
* **Machine Learning:** Scikit-learn (Linear Regression, Decision Tree Regressor, Gradient Boosting Regressor)
* **Visualization:** Matplotlib, Seaborn, Folium (for geographic plotting)
* **Frontend:** HTML templates with embedded base64 encoded static plots

## 🚀 Features
* **Transit Time Analysis:** Evaluate and visualize total transit duration.
* **Waiting & Dwell Time Analysis:** Track operational delays before and during port visits.
* **Geospatial Mapping:** Interactive Folium map generation for vessel locations.
* **Speed & Vessel Type Analysis:** Discover patterns specific to vessel classifications and movement speed.
* **Source & Destination Tracking:** Frequency distribution of common routes and port calls.

## 📂 Project Structure
```
port-efficiency-decision-support-system/
├── src/                      # Main source code
│   ├── app.py                # Flask application entry point
│   ├── analytics.py          # Core visualization and ML logic
│   └── preprocessing.py      # Script for cleaning and feature engineering
├── templates/                # Frontend HTML templates
├── docs/                     # Project documentation and academic reports
├── sample_data/              # Directory for placing compatible local datasets
├── static/                   # Static assets (including screenshots)
│   └── screenshots/          # [TODO: Add project screenshots here]
├── .gitignore                
├── requirements.txt          # Python dependencies
└── README.md                 
```

## 🛠 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/veera491/port-efficiency-decision-support-system.git
   cd port-efficiency-decision-support-system
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Data:**
   * Place your AIS dataset in the root directory or `sample_data/` folder.
   * Run the preprocessing script if required:
     ```bash
     python src/preprocessing.py
     ```
   *(Ensure paths in `src/app.py` match your data location, default expects `PreProcessedData.csv` in the root).*

5. **Run the Application:**
   ```bash
   python src/app.py
   ```
   The Flask server will start, typically accessible at `http://127.0.0.1:5000/`.

## 📸 Screenshots
*(TODO: Add screenshots of the interactive maps and analytics dashboards here)*

## 🤝 Contribution Guidelines
This is an academic project. Contributions, bug reports, and feature requests are welcome via GitHub Issues and Pull Requests. Ensure code aligns with the existing standard and update documentation for any substantial changes.

## 📝 License
[MIT License](LICENSE) (or add appropriate academic license).
