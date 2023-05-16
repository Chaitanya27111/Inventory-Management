import pandas as pd
from sklearn.model_selection import train_test_split

# specify the input file name
input_file = "dataset_1_item.csv"

# specify the output file names
train_file = "train.csv"
test_file = "test.csv"

# specify the split ratio (0.8 means 80% for training and 20% for testing)
split_ratio = 0.7

# read the input CSV file into a pandas DataFrame
data = pd.read_csv(input_file)

# split the DataFrame into training and testing datasets randomly
train_data, test_data = train_test_split(data, test_size=1-split_ratio, random_state=42)

# save the training and testing datasets as separate CSV files
train_data.to_csv(train_file, index=False)
test_data.to_csv(test_file, index=False)
