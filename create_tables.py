import sqlalchemy as sq
import os

"""
R1: Hospital (Hospital_ID, name, street, zipcode, state, patient-nurse ratio, infection_rating)
    Null values are allowed for patient-nurse ratio not all hospitals publish this data
R2: Insurance(Hospital_ID (FK), Insurance company) 
R3: Department (Hospital_ID (FK), Department Name, ranking, wait times) 
    Null values are allowed for ranking because not all departments have rankings
R4: Inpatient (Hospital_ID (FK), Inpatient Medical Procedure name, cost of procedure, cost of stay per night)
R5: Outpatient( Hospital_ID (FK), Outpatient Medical Procedure name, cost of procedure)
R6: Doctor(Doctor_ID, name, specialization)
R7: Phone_Number(Doctor_ID (FK), Phone_Number) 
R8: Credential(Doctor_ID (FK), Place_Of_Education)
R9: Reviews(Doctor_ID (FK), review)
    Null values are allowed for review because a doctor can have no reviews
R10: Performs(Hospital_ID (FK), department name (FK), In Medical Procedure name (FK))
R11: Performs(Hospital_ID (FK), department name (FK), Out Medical Procedure name (FK))
"""

oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'

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

# Create all tables

# R1: Hospital (Hospital_ID, name, street, zipcode, state, patient-nurse ratio, infection_rating)
hospitals = sq.Table('hospitals', metadata, sq.Column('Hospital_ID', sq.Integer(), primary_key=True),  # maybe do a sequence here
                     sq.Column('Hospital_Name', sq.String(225), nullable=False),
                     sq.Column('Street', sq.String(225), nullable=False),
                     sq.Column('Zipcode', sq.Integer(), nullable=False),
                     sq.Column('State', sq.String(225), nullable=False),  # Look into char
                     sq.Column('Patient_Nurse_Ratio', sq.String(225), nullable=True),
                     sq.Column('Infection_Rating', sq.Float(), nullable=True))


# Use a sequence here:

# R2: Insurance(Hospital_ID (FK), Insurance company)
insurance = sq.Table('insurance', metadata,
                     sq.Column('Hospital_ID', sq.Integer(), sq.ForeignKey("hospitals.Hospital_ID"), primary_key=True),
                     sq.Column('Insurance_Company_Name', sq.String(255), nullable=False, primary_key=True))

metadata.create_all(engine)
