import pandas as pd

# Read the CSV file into a pandas dataframe
df = pd.read_csv('test.csv')

# Identify the column containing the dates and convert it to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert the date column to the desired format
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Write the updated dataframe to a new CSV file
df.to_csv('new_file_test.csv', index=False)
