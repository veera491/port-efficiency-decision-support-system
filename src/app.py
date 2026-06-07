from flask import Flask, render_template, request, send_file
from flask_cors import CORS
import pandas as pd
import analytics as A
from pytz import utc
import base64
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/static')
CORS(app)

def img_to_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/api', methods=['POST'])
def page():
    from_date = request.form.get('fromDate')
    from_date = pd.to_datetime(from_date).tz_localize(None).tz_localize(utc)
    to_date = request.form.get('toDate')
    to_date = pd.to_datetime(to_date).tz_localize(None).tz_localize(utc)
    data_type = request.form.get('dataType')

    df = pd.read_csv('PreProcessedData.csv')
    df['TimePosition'] = pd.to_datetime(df['TimePosition'])
    df = df.sort_values(by='TimePosition')
    df = df[(pd.to_datetime(from_date) < df['TimePosition']) & (df['TimePosition'] < pd.to_datetime(to_date))]

    if data_type == 'TransitTime':
        ml_results = {
            "Linear Regression": {'MSE': 313.43353903714865, 'R2': 0.9981581950402982, 'MAE': 12.512719764245322},
            "Decision Tree Regression": {'MSE': 7.75568474538117, 'R2': 0.9999544258770973, 'MAE': 0.5137088719674724},
            "Gradient Boosting Regression": {'MSE': 191.67700337670288, 'R2': 0.9988736634357495,
                                             'MAE': 9.429212350949546}
        }
        avg_time, median_time, std_time = [round(i, 2) for i in
                                           A.AnalyzeTime(df, 'SD/TransitTime', 'TransitTime')]

        return render_template('TransitTime.html',
                               from_date=from_date, to_date=to_date, ml_results=ml_results,
                               specified_dates={'mean': avg_time, 'median': median_time, 'std_dev': std_time},
                               TransitTimedistribution=img_to_base64('./SD/TransitTime/TransitTimedistribution.png'),
                               avg_TransitTime_by_vessel_type=img_to_base64('./SD/TransitTime/avg_TransitTime_by_vessel_type.png'),
                               speed_vs_TransitTime=img_to_base64('./SD/TransitTime/speed_vs_TransitTime.png'),
                               TransitTime_by_nav_status=img_to_base64('./SD/TransitTime/TransitTime_by_nav_status.png'),
                               TransitTime_trend=img_to_base64('./SD/TransitTime/TransitTime_trend.png')
                               )

    elif data_type == 'WaitingTime':
        ml_results = {'Linear Regression': {'MSE': 39948.20130259924, 'R2': 0.0059837025171914915, 'MAE': 38.36027729266752}, 'Decision Tree Regression': {'MSE': 69752.56518016118, 'R2': -0.7356272452697581, 'MAE': 28.579752446725404}, 'Gradient Boosting Regression': {'MSE': 34225.584331421705, 'R2': 0.1483774611376093, 'MAE': 24.495346349085956}}

        avg_time, median_time, std_time = [round(i, 2) for i in
                                           A.AnalyzeTime(df, 'SD/WaitingTime', 'WaitingTime')]

        return render_template('WaitingTime.html',
                               from_date=from_date, to_date=to_date, ml_results=ml_results,
                               specified_dates={'mean': avg_time, 'median': median_time, 'std_dev': std_time},
                               WaitingTimedistribution=img_to_base64('./SD/WaitingTime/WaitingTimedistribution.png'),
                               avg_WaitingTime_by_vessel_type=img_to_base64(
                                   './SD/WaitingTime/avg_WaitingTime_by_vessel_type.png'),
                               speed_vs_WaitingTime=img_to_base64('./SD/WaitingTime/speed_vs_WaitingTime.png'),
                               WaitingTime_by_nav_status=img_to_base64(
                                   './SD/WaitingTime/WaitingTime_by_nav_status.png'),
                               WaitingTime_trend=img_to_base64('./SD/WaitingTime/WaitingTime_trend.png')
                               )

    elif data_type == 'DwellTime':
        ml_results = {'Linear Regression': {'MSE': 313.97966566643026, 'R2': 0.9981597728068103, 'MAE': 12.525869977412405}, 'Decision Tree Regression': {'MSE': 34.383258223739944, 'R2': 0.9997984805587983, 'MAE': 1.18439438085724}, 'Gradient Boosting Regression': {'MSE': 291.8090756978517, 'R2': 0.9982897140960421, 'MAE': 12.121966969336297}}


        avg_time, median_time, std_time = [round(i, 2) for i in
                                           A.AnalyzeTime(df, 'SD/DwellTime', 'DwellTime')]

        return render_template('DwellTime.html',
                               from_date=from_date, to_date=to_date, ml_results=ml_results,
                               specified_dates={'mean': avg_time, 'median': median_time, 'std_dev': std_time},
                               DwellTimedistribution=img_to_base64('./SD/DwellTime/DwellTimedistribution.png'),
                               avg_DwellTime_by_vessel_type=img_to_base64(
                                   './SD/DwellTime/avg_DwellTime_by_vessel_type.png'),
                               speed_vs_DwellTime=img_to_base64('./SD/DwellTime/speed_vs_DwellTime.png'),
                               DwellTime_by_nav_status=img_to_base64(
                                   './SD/DwellTime/DwellTime_by_nav_status.png'),
                               DwellTime_trend=img_to_base64('./SD/DwellTime/DwellTime_trend.png')
                               )
    elif data_type == 'ShipsLocations':
        return send_file('./templates/ship_locations_map.html')
    elif data_type == 'SpeedAnalysis':
        ml_results = {'Linear Regression': {'MSE': 6.136187598811394, 'R2': 0.346484173044725, 'MAE': 1.8156972783357443}, 'Decision Tree Regression': {'MSE': 0.2678459446215094, 'R2': 0.9714738897438779, 'MAE': 0.20196510448520955}, 'Gradient Boosting Regression': {'MSE': 3.178040299553715, 'R2': 0.6615325719731352, 'MAE': 1.2876548037467692}}

        avg_time, median_time, std_time = [round(i, 2) for i in
                                           A.AnalyzeSpeed(df, 'SD/speed')]

        return render_template('speed.html',
                               from_date=from_date, to_date=to_date, ml_results=ml_results,
                               specified_dates={'mean': avg_time, 'median': median_time, 'std_dev': std_time},
                               speed_distribution=img_to_base64('./SD/speed/speed_distribution.png'),
                               speed_by_vessel_type=img_to_base64(
                                   './SD/speed/speed_by_vessel_type.png'),
                               speed_by_vessel_name=img_to_base64(
                                   './SD/speed/speed_by_vessel_name.png')
                               )
    elif data_type == 'VesselTypeAnalysis':

        A.AnalyzeVesselType(df, 'SD/VesselType')
        return render_template('VesselType.html',
                               from_date=from_date, to_date=to_date,
                               vessel_type_distribution=img_to_base64('./SD/VesselType/vessel_type_distribution.png'),
                               speed_by_vessel_type=img_to_base64(
                                   './SD/VesselType/speed_by_vessel_type.png'),
                               transit_time_by_vessel_type=img_to_base64(
                                   './SD/VesselType/transit_time_by_vessel_type.png')
                               )

    elif data_type == 'LengthWidthAnalysis':
        A.AnalyzeLengthWidth(df, 'SD/LW')
        return render_template('LengthWidth.html',
                               from_date=from_date, to_date=to_date,
                               vessel_length_distribution=img_to_base64('./SD/LW/vessel_length_distribution.png'),
                               vessel_width_distribution=img_to_base64(
                                   './SD/LW/vessel_width_distribution.png'),
                               length_by_vessel_type=img_to_base64(
                                   './SD/LW/length_by_vessel_type.png'),
                               width_by_vessel_type=img_to_base64(
                                   './SD/LW/width_by_vessel_type.png')
                               )

    elif data_type == 'SourceDestinationAnalysis':
        A.AnalyzeSourceDestination(df, 'SD/SourceDestination')
        return render_template('SourceDestination.html',
                               from_date=from_date, to_date=to_date,
                               source_position_frequency=img_to_base64('./SD/SourceDestination/source_position_frequency.png'),
                               destination_frequency=img_to_base64(
                                   './SD/SourceDestination/destination_frequency.png')
                               )


if __name__ == '__main__':
    app.run(debug=True)
