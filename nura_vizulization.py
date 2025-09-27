# Required libraries
import pandas as pd
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# ------------------------------
# Step 1: Connect to MySQL
# ------------------------------
# Replace these with your MySQL credentials
user = 'root'
password = 'pass123'
host = 'localhost'  # or your host
port = 3306
database = 'nura'

# Create connection using SQLAlchemy
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# Load table
df = pd.read_sql('SELECT * FROM messages_with_statuses', con=engine, parse_dates=['sent_at', 'read_at'])

# ------------------------------
# Step 2: Preprocess Data
# ------------------------------
# Convert sent_at and read_at to datetime (if not already)
df['sent_at'] = pd.to_datetime(df['message_inserted_at'])
df['read_at'] = pd.to_datetime(df['status_timestamp'])

# Create week column
df['week'] = df['sent_at'].dt.to_period('W').apply(lambda r: r.start_time)

# ------------------------------
# Step 3a: Total and Active Users Over Time
# ------------------------------
total_users = df.groupby('week')['author_type'].nunique().reset_index(name='total_users')
active_users = df[df['direction'] == 'inbound'].groupby('week')['author_type'].nunique().reset_index(name='active_users')
users_over_time = pd.merge(total_users, active_users, on='week')

fig1 = px.line(users_over_time, x='week', y=['total_users', 'active_users'],
               title='Total and Active Users Over Time')
fig1.show()

# ------------------------------
# Step 3b: Fraction of Non-Failed Outbound Messages Read
# ------------------------------
outbound = df[(df['direction'] == 'outbound') & (df['status'] != 'failed')]
read_fraction = outbound['read_at'].notna().mean()
print(f"Fraction of outbound messages read: {read_fraction:.2%}")

# Optional: Fraction read per week
read_by_week = outbound.groupby('week')['read_at'].apply(lambda x: x.notna().mean()).reset_index()
fig2 = px.bar(read_by_week, x='week', y='read_at', labels={'read_at': 'Fraction Read'}, title='Fraction of Outbound Messages Read Over Time')
fig2.show()

# ------------------------------
# Step 3c: Distribution of Time to Read
# ------------------------------
read_outbound = outbound[outbound['read_at'].notna()].copy()
read_outbound['time_to_read_hours'] = (read_outbound['read_at'] - read_outbound['sent_at']).dt.total_seconds() / 3600

fig3 = px.histogram(read_outbound, x='time_to_read_hours', nbins=50, title='Distribution of Time to Read (hours)')
fig3.show()

# ------------------------------
# Step 3d: Number of Outbound Messages in Last Week by Status
# ------------------------------
last_week_start = datetime.now() - timedelta(days=7)
last_week_msgs = df[(df['direction'] == 'outbound') & (df['sent_at'] >= last_week_start)]
status_counts = last_week_msgs['status'].value_counts().reset_index()
status_counts.columns = ['status', 'count']

fig4 = px.bar(status_counts, x='status', y='count', title='Outbound Messages in Last Week by Status')
fig4.show()
