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
R6: Doctor(Doctor_ID, name)
R7: Specializations(Doctor_ID (FK), Specialization)
R8: Phone_Number(Doctor_ID (FK), Phone_Number) 
R9: Credential(Doctor_ID (FK), Place_Of_Education)
R10: Reviews(Doctor_ID (FK), review)
    Null values are allowed for review because a doctor can have no reviews
R11: Performs(Hospital_ID (FK), department name (FK), In Medical Procedure name (FK))
R12: Performs(Hospital_ID (FK), department name (FK), Out Medical Procedure name (FK))
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
                     sq.Column('Insurance_Company_Name', sq.String(225), nullable=False, primary_key=True))

# R3: Department (Hospital_ID (FK), Department Name, ranking, wait times)
hospital_departments = sq.Table('hospital_departments', metadata,
                                sq.Column('Hospital_ID', sq.Integer(), sq.ForeignKey("hospitals.Hospital_ID"), primary_key=True),
                                sq.Column('Department_Name', sq.String(225), nullable=False, primary_key=True),
                                sq.Column('Ranking', sq.Float(), nullable=True),
                                sq.Column('Wait_Time', sq.Integer()))

# R4: Inpatient (Hospital_ID (FK), Inpatient Medical Procedure name, cost of procedure, cost of stay per night)
inpatients = sq.Table('inpatients', metadata,
                     sq.Column('Hospital_ID', sq.Integer(), sq.ForeignKey("hospitals.Hospital_ID"), primary_key=True),
                     sq.Column('Inpatient_Procedure_Name', sq.String(225), nullable=False, primary_key=True),
                     sq.Column('Cost_of_procedure', sq.Float(), nullable=False),
                     sq.Column('Cost_of_stay_per_night', sq.Float(), nullable=True))

# R5: Outpatient( Hospital_ID (FK), Outpatient Medical Procedure name, cost of procedure)
outpatients = sq.Table('outpatients', metadata,
                      sq.Column('Hospital_ID', sq.Integer(), sq.ForeignKey("hospitals.Hospital_ID"), primary_key=True),
                      sq.Column('Outpatient_Procedure_Name', sq.String(225), nullable=False, primary_key=True),
                      sq.Column('Cost_of_procedure', sq.Float(), nullable=False))


# R6: Doctors(Doctor_ID, name)
doctors = sq.Table('doctors', metadata,
                   sq.Column('Doctor_ID', sq.Integer(), primary_key=True),
                   sq.Column('Doctor_Name', sq.String(225), nullable=False))


# R7: Specializations(Doctor_ID (FK), Specialization)
specializations = sq.Table('specializations', metadata,
                           sq.Column('Doctor_ID', sq.Integer(), sq.ForeignKey("doctors.Doctor_ID"), primary_key=True),
                           sq.Column('Specialization', sq.String(225), primary_key=True))

# R8: Phone_Number(Doctor_ID (FK), Phone_Number)
phone_numbers = sq.Table('phone_numbers', metadata,
                         sq.Column('Doctor_ID', sq.Integer(), sq.ForeignKey("doctors.Doctor_ID"), primary_key=True),
                         sq.Column('Phone_Number', sq.Integer(), primary_key=True))  # Will need to make this more readable to the user

# R9: Credential(Doctor_ID (FK), Place_Of_Education)
credentials = sq.Table('credentials', metadata,
                       sq.Column('Doctor_ID', sq.Integer(), sq.ForeignKey("doctors.Doctor_ID"), primary_key=True),
                       sq.Column('Place_Of_Education', sq.String(255), primary_key=True))

# R10: Reviews(Doctor_ID (FK), review)
#     Null values are allowed for review because a doctor can have no reviews
reviews = sq.Table('reviews', metadata,
                   sq.Column('Doctor_ID', sq.Integer(), sq.ForeignKey("doctors.Doctor_ID"), primary_key=True),
                   sq.Column('Review', sq.String(500), primary_key=True, default="No reviews"))


# R11: Performs(Hospital_ID (FK), department name (FK), In Medical Procedure name (FK))
# Constraints are needed because Department_Name and Inpatient_Procedure_Name are part of composite keys
performs_inpatients = sq.Table('performs_inpatients', metadata,
                               sq.Column('Hospital_ID', sq.Integer(), sq.ForeignKey("hospitals.Hospital_ID"), primary_key=True),
                               sq.Column('Department_Name', sq.String(225), primary_key=True),
                               sq.Column('Inpatient_Procedure_Name', sq.String(225), primary_key=True),
                               sq.ForeignKeyConstraint(['Hospital_ID', 'Department_Name'],
                                                       ['hospital_departments.Hospital_ID', 'hospital_departments.Department_Name'],
                                                       name='fk_inpatient_department_name'),
                               sq.ForeignKeyConstraint(['Hospital_ID', 'Inpatient_Procedure_Name'],
                                                       ['inpatients.Hospital_ID', 'inpatients.Inpatient_Procedure_Name'],
                                                       name='fk_inpatient_procedure'))


# R12: Performs(Hospital_ID (FK), department name (FK), Out Medical Procedure name (FK))
# Constraints are needed because Department_Name and Inpatient_Procedure_Name are part of composite keys
performs_outpatients = sq.Table('performs_outpatients', metadata,
                               sq.Column('Hospital_ID', sq.Integer(), sq.ForeignKey("hospitals.Hospital_ID"), primary_key=True),
                               sq.Column('Department_Name', sq.String(225), primary_key=True),
                               sq.Column('Outpatient_Procedure_Name', sq.String(225), primary_key=True),
                               sq.ForeignKeyConstraint(['Hospital_ID', 'Department_Name'],
                                                       ['hospital_departments.Hospital_ID', 'hospital_departments.Department_Name'],
                                                       name='fk_outpatient_department_name'),
                               sq.ForeignKeyConstraint(['Hospital_ID', 'Outpatient_Procedure_Name'],
                                                       ['outpatients.Hospital_ID', 'outpatients.Outpatient_Procedure_Name'],
                                                       name='fk_outpatient_procedure'))

metadata.create_all(engine)
