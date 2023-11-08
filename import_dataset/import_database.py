import pandas as pd
from sqlalchemy import create_engine
import random

# Function to truncate sentences to 700 characters and ensure they end with a dot
def truncate_and_dot(sentence):
    if type(sentence)==str:
        if len(sentence) > 700:
            sentence = sentence[:700]
            if '.' in sentence:
                # The rfind method in Python is used to find the last occurrence of a substring within a string. 
                last_period = sentence.rfind('.')
                sentence = sentence[:last_period + 1]
            else:
                sentence = sentence[:699] + '.'
        else:
            if not sentence.endswith('.'):
                sentence += '.'

    return sentence

data = pd.read_csv ("./import_dataset/datasetBooks.csv")   
df = pd.DataFrame(data)

'''
# List of the 20 most spoken languages in the world
languages = ['Mandarin Chinese', 'Hindi', 'Spanish', 'French', 'Standard Arabic', 'Bengali', 'Russian', 'Portuguese', 'Indonesian', 'Urdu', 'German', 'Japanese', 'Swahili', 'Marathi', 'Telugu', 'Turkish', 'Tamil', 'Vietnamese', 'Korean']

# Add a new column with randomly selected languages
df['language'] = df.apply(lambda row: ['English'] + random.sample([lang for lang in languages if lang != 'English'], k=random.randint(0, 9)), axis=1)

# Save the updated dataset
# Replace 'updated_dataset.csv' with the desired filename for your updated dataset
df.to_csv('./import_dataset/datasetBooks.csv', index=False)
'''
integer_columns = ['pages', 'numRatings']
float_columns = ['rating', 'likedPercent', 'bbeScore', 'price']

for column_name in integer_columns:
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce', downcast='integer').fillna(0).astype(int)

for column_name in float_columns:
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce', downcast='float').fillna(0).astype(float)


# Apply the function to each cell in the DataFrame
truncated_df = df.applymap(truncate_and_dot)

# Replacing bookId with numerical incremental values
truncated_df['bookId'] = [f'book_{i+1}' for i, _ in enumerate(truncated_df['bookId'])]

# Replace 'your_username', 'your_password', 'your_host', 'your_database' with your MySQL credentials
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/AICHALLENGE')

# Replace 'df' with your DataFrame variable name
truncated_df.to_sql('Book', con=engine, if_exists='replace', index=False)