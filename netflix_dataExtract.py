import pandas as pd

df = pd.read_csv('netflix_titles.csv')

# For windows
# import sqlalchemy as sal
# engine = sal.create_engine('mssql://user\SQLEXPRESS/master?driver=ODBC+DRIVER+17+FOR+SQL+SERVER')
# conn=engine.connect()
# df.to_sql('netflix_raw', con=conn , index=False, if_exists = 'append')
# conn.close()

# In mac use the below code
import sqlalchemy as sal
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# 1. Build connection URL matching your Docker parameters
connection_url = URL.create(
    "mssql+pymssql",
    username="userZ",
    password="Password",                       # Must match MSSQL_SA_PASSWORD above
    host="localhost",                             # Localhost points to your mapped Docker port
    port=1433,
    database="master",                            # Connect to default system DB first
)

conn = create_engine(connection_url)

# 2. Verify connection
try:
    with conn.connect() as connection:
        print("Connected successfully to MS SQL Server inside Docker!")

except Exception as e:
    print(f"Connection failed: {e}")


df.to_sql('tNetflix_rawdata', con=conn , index=False, if_exists = 'append')

# By default SQL table crreates columns to max length
# Let's analyse the column's and fix the column size issue

print('Max length of show_id: ',max(df.show_id.str.len()))
print('Max length of type: ',max(df.type.str.len()))

# Title field contains foreign letters so let's keep it as nvarchar type in sql
print('Max length of title: ',max(df.title.str.len())) 
print('Max length of director: ',max(df.director.str.len()))
print('Max length of cast with null: ',max(df.cast.str.len()))
# As cast column contains null values it returns 'nan'
# To avoid the null value and get the max length use dropna()
print('Max length of cast without null: ',max(df.cast.dropna().str.len()))

print('Max length of date_added: ',max(df.date_added.str.len()))

print('Max length of country: ',max(df.country.str.len()))
print('Max length of rating: ',max(df.rating.str.len()))
print('Max length of duration: ',max(df.duration.str.len()))
print('Max length of listed_in: ',max(df.listed_in.str.len()))
print('Max length of description: ',max(df.description.str.len()))

# print(df.loc[df.show_id=='s5023'])