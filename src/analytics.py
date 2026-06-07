import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
import folium
from folium.plugins import FastMarkerCluster

import matplotlib
matplotlib.use('Agg')



def AnalyzeTime(df, TimeLine, col):
    output_dir = TimeLine

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Convert Time to minutes
    df[col] = abs(pd.to_timedelta(df[col]).dt.total_seconds() / 60)  # Convert to minutes

    # Compute average time
    avg_time = df[col].mean()

    # Compute median time
    median_time = df[col].median()

    # Compute standard deviation of time
    std_time = df[col].std()

    # Transit Time Distribution Analysis (Histogram)
    #plt.figure(figsize=(8, 6))
    sns.histplot(df[col], bins=5, kde=True, color='skyblue', edgecolor='black')
    plt.title(col + ' Distribution')
    plt.xlabel(col + ' (minutes)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, col + 'distribution.png'))
    plt.close()

    # Vessel Type vs. Average col Time Analysis
    avg_time_by_vessel_type = df.groupby('VesselType')[col].mean().reset_index()

    #plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_time_by_vessel_type, x='VesselType', y=col, palette='Set2')
    plt.title('Average ' + col + ' by Vessel Type')
    plt.xlabel('Vessel Type')
    plt.ylabel('Average ' + col + ' (minutes)')
    plt.xticks(rotation=90)
    plt.savefig(os.path.join(output_dir, 'avg_' + col + '_by_vessel_type.png'))
    plt.close()

    # Impact of Speed on col Time (Scatter Plot with Regression Line)
    df = df.dropna(subset=[col, 'Speed'])  # Drop rows with NaN values
    X = np.array(df['Speed']).reshape(-1, 1)
    y = np.array(df[col])

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    #plt.figure(figsize=(15, 15))
    plt.scatter(df['Speed'], df[col], color='blue')
    plt.plot(df['Speed'], y_pred, color='red', linewidth=2)
    plt.title('Impact of Speed on Transit Time')
    plt.xlabel('Speed (knots)')
    plt.ylabel(col + ' (minutes)')
    plt.savefig(os.path.join(output_dir, 'speed_vs_' + col + '.png'))
    plt.close()

    # Root Cause Analysis of Delays (example with Navigation Status)
    #plt.figure(figsize=(15, 15))
    sns.boxplot(data=df, x='NavStatus', y=col, palette='Set3')
    plt.title(col + ' by Navigation Status')
    plt.xlabel('Navigation Status')
    plt.ylabel(col + ' (minutes)')
    plt.xticks(rotation=90)
    plt.savefig(os.path.join(output_dir, col + '_by_nav_status.png'))
    plt.close()

    # Trend Analysis
    df.set_index('TimePosition', inplace=True)
    df[col].rolling(window=2).mean().plot(figsize=(15, 15))
    plt.title(col + ' Trend Analysis')
    plt.xlabel('Time Position')
    plt.ylabel('Rolling Mean of ' + col + ' (minutes)')
    plt.savefig(os.path.join(output_dir, col + '_trend.png'))
    plt.close()

    # Return computed values or insights as needed
    return avg_time, median_time, std_time


"""AnalyzeTransitTime(
    pd.read_csv('PreProcessedData.csv'),
    'TransitTime/BC',
    'TransitTime'
)"""


def create_ship_location_map(df, TimeLine):
    output_dir = 'maps' + TimeLine
    os.makedirs(output_dir, exist_ok=True)

    # Create a base map centered at the average latitude and longitude of the ships
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    ship_map = folium.Map(location=map_center, zoom_start=8)

    # Prepare data for FastMarkerCluster
    data = df.apply(lambda row: [row['Latitude'], row['Longitude'], f"Name: {row['Name']}<br>VesselType: {row['VesselType']}<br>TransitTime: {row['TransitTime']}"], axis=1).tolist()

    # Add FastMarkerCluster to the map
    FastMarkerCluster(data).add_to(ship_map)

    # Save the map to an HTML file
    map_output_path = os.path.join(output_dir, 'ship_locations_map.html')
    ship_map.save(map_output_path)
    print(f"Ship locations map saved to {map_output_path}")


"""# Call the function to create the map
create_ship_location_map(df, '/BC')"""


def AnalyzeSpeed(df, TimeLine):
    output_dir = TimeLine

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Compute average speed
    avg_speed = df['Speed'].mean()

    # Compute median speed
    median_speed = df['Speed'].median()

    # Compute standard deviation of speed
    std_speed = df['Speed'].std()

    # Speed Distribution Analysis (Histogram)
    sns.histplot(df['Speed'], bins=20, kde=True, color='skyblue', edgecolor='black')
    plt.title('Speed Distribution')
    plt.xlabel('Speed (knots)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'speed_distribution.png'))
    plt.close()


    # Vessel-Specific Speed Analysis
    sns.boxplot(data=df, x='VesselType', y='Speed', palette='Set2')
    plt.title('Speed by Vessel Type')
    plt.xlabel('Vessel Type')
    plt.ylabel('Speed (knots)')
    plt.xticks(rotation=90)
    plt.savefig(os.path.join(output_dir, 'speed_by_vessel_type.png'))
    plt.close()

    # Vessel-Specific Speed Analysis by Vessel Name
    sns.boxplot(data=df, x='Name', y='Speed', palette='Set2')
    plt.title('Speed by Vessel Name')
    plt.xlabel('Vessel Name')
    plt.ylabel('Speed (knots)')
    plt.xticks(rotation=90)
    plt.savefig(os.path.join(output_dir, 'speed_by_vessel_name.png'))
    plt.close()

    # Return computed values or insights as needed
    return avg_speed, median_speed, std_speed


# AnalyzeSpeed(df, 'BC')


def AnalyzeVesselType(df, TimeLine):
    output_dir = TimeLine

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Distribution Analysis: Frequency of each vessel type
    vessel_type_counts = df['VesselType'].value_counts()
    sns.barplot(x=vessel_type_counts.index, y=vessel_type_counts.values, palette='Set2')
    plt.title('Vessel Type Distribution')
    plt.xlabel('Vessel Type')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'vessel_type_distribution.png'))
    plt.close()

    # Comparison of Speed by Vessel Type
    sns.boxplot(data=df, x='VesselType', y='Speed', palette='Set2')
    plt.title('Speed by Vessel Type')
    plt.xlabel('Vessel Type')
    plt.ylabel('Speed (knots)')
    plt.savefig(os.path.join(output_dir, 'speed_by_vessel_type.png'))
    plt.close()

    # Comparison of Transit Time by Vessel Type
    # Convert Time to hours
    df['TransitTime'] = abs(pd.to_timedelta(df['TransitTime']).dt.total_seconds() / 60)

    sns.boxplot(data=df, x='VesselType', y='TransitTime', palette='Set2')
    plt.title('Transit Time by Vessel Type')
    plt.xlabel('Vessel Type')
    plt.ylabel('Transit Time (hours)')
    plt.savefig(os.path.join(output_dir, 'transit_time_by_vessel_type.png'))
    plt.close()


def AnalyzeLengthWidth(df, TimeLine):
    output_dir = TimeLine

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Distribution Analysis: Vessel Length
    sns.histplot(df['Length'], bins=20, kde=True, color='skyblue', edgecolor='black')
    plt.title('Distribution of Vessel Length')
    plt.xlabel('Length')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'vessel_length_distribution.png'))
    plt.close()

    # Distribution Analysis: Vessel Width
    sns.histplot(df['Width'], bins=20, kde=True, color='skyblue', edgecolor='black')
    plt.title('Distribution of Vessel Width')
    plt.xlabel('Width')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'vessel_width_distribution.png'))
    plt.close()

    # Comparison of Length by Vessel Type
    sns.boxplot(data=df, x='VesselType', y='Length', palette='Set2')
    plt.title('Length by Vessel Type')
    plt.xlabel('Vessel Type')
    plt.ylabel('Length')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, 'length_by_vessel_type.png'))
    plt.close()

    # Comparison of Width by Vessel Type
    sns.boxplot(data=df, x='VesselType', y='Width', palette='Set2')
    plt.title('Width by Vessel Type')
    plt.xlabel('Vessel Type')
    plt.ylabel('Width')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, 'width_by_vessel_type.png'))
    plt.close()


# AnalyzeLengthWidth(df, 'BC')

def AnalyzeSourceDestination(df, TimeLine):
    output_dir = TimeLine

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Frequency Analysis: Source Position
    sns.countplot(data=df, x='SourcePosition', palette='Set2')
    plt.title('Frequency of Source Positions')
    plt.xlabel('Source Position')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'source_position_frequency.png'))
    plt.close()

    # Frequency Analysis: Destination
    destination_count = df['Destination'].value_counts().sort_values(ascending=False).head(20)

    plt.bar(destination_count.index, list(destination_count))
    plt.ylim(0, 19000)

    plt.title('Frequency of Top 20 Destinations')
    plt.xlabel('Destination')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, 'destination_frequency.png'))
    plt.close()

# AnalyzeSourceDestination(df, 'BC')
