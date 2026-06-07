import pandas as pd

# Data Collection
df = pd.read_csv('PRJ912.csv')
print('Data Read Completed')

# Handling Null Values
df = df.dropna()
print('Removing Null Values Completed')

# Handling Duplicates
df = df.drop_duplicates()
print('Removing duplicates Completed')

# Remove Unwanted columns
df = df.drop(['DimA', 'DimB', 'DimC', 'DimD'], axis=1)
print('Removing Unwanted columns Completed')

# Feature Engineering
df['TimePosition'] = pd.to_datetime(df['TimePosition'])
df['TimeETA'] = pd.to_datetime(df['TimeETA'])
df['TimeVoyage'] = pd.to_datetime(df['TimeVoyage'])

df['TransitTime'] = df['TimeETA'] - df['TimePosition']
df = df.sort_values(by=['MMSI', 'TimePosition'])
df['WaitingTime'] = df.groupby('MMSI')['TimePosition'].diff()
df['DwellTime'] = df['TimeETA'] - df['TimeVoyage']

print('Feature Engineering Completed')

# Save the preprocessed data
df.to_csv('PreProcessedData.csv', index=False, header=True)
print('Data saved into a .CSV file')
