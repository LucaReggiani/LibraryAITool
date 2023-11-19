import pandas as pd
from sqlalchemy import create_engine


# Define your MySQL database connection
# Replace 'username', 'password', 'hostname', 'database' with your actual MySQL credentials
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/AICHALLENGE')

csv_file_path = './datasetBooksFinalVersion.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Replace 'your_table' with the actual name of your table
table_name = 'Book'

df.to_sql('Book', engine, if_exists='append', index=False)

# Close the database connection
engine.dispose()



