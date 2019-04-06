from flask import Flask, render_template
import cx_Oracle
import pandas as pd
import sqlalchemy as sq
import os

app = Flask(__name__)
oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'

print(os.environ.get('DB_USER'))
# Physically connect to the Oracle Database
engine = sq.create_engine(
    oracle_connection_string.format(
        username=os.environ.get('HOSPITAL_USER'),
        password=os.environ.get('HOSPITAL_PASS'),
        hostname=os.environ.get('DB_HOST'),
        port='1521',
        database=os.environ.get('DB_SID'),
    )
)

connection = engine.connect()
# MetaData object contains all the schema constructs
metadata = sq.MetaData()

# Access a table by:
employees = sq.Table('employees', metadata, autoload=True, autoload_with=engine)

# Access columns
print(employees.columns.keys())

# Access all contents
# ------

# Select * from employees
query = sq.select([employees])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()

# df = pd.DataFrame(ResultSet)
# print(df)


# Filtering queries (using where)
query2 = sq.select([employees]).where(employees.columns.last_name == 'King')
ResultProxy2 = connection.execute(query2)
ResultSet2 = ResultProxy2.fetchall()

df2 = pd.DataFrame(ResultSet2)
print(df2)


@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Nikhita'}

    posts = [
        {
            'author': {'username' : 'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'Suzy'},
            'body': 'Not really'
        },
        {
            'author': {'username': 'Adam'},
            'body': '...'
        }
    ]
    return render_template('index.html', user=user, posts=posts)


if __name__ == '__main__':
    app.run()
