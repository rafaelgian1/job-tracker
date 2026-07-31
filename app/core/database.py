import sqlalchemy as db

engine = db.create_engine("postgresql+psycopg2://admin:2026jobanalysis@localhost:5432/job_tracker_db")
conn = engine.connect()

metadata = db.MetaData()
users = db.Table('users', metadata, autoload=True,
                 autoload_with=engine)

print(repr(metadata.tables['users']))


db.Table('users', db.Metadata(), db.Column('id', db.Integer(), primary_key=True, table=users),
db.Column('email', db.String(255), table=users),
db.Column('hashed_password', db.String(255), table=users),
db.Column('created_at', db.Datetime(), table=users), schema=None)

jobs = db.Table('jobs', metadata, autoload = True,
                autoload_with=engine)

print(repr(metadata.tables['jobs']))

db.Table('jobs', db.Metadata(), db.Column('id', db.Integer(), table=jobs),
         db.Column('user_id', db.Integer(), foreign_key=users.id, table=jobs),
         db.Column('company', db.String(255), table=jobs),
         db.Column('title', db.String(255), table=jobs),
         db.Column('location', db.String(255), table=jobs),
         db.Column('status', db.String(255), table=jobs),
         db.Column('status', db.String(255), table=jobs),
         db.Column('url', db.String(255), table=jobs),
         db.Column('salary_range', db.String(255), table=jobs),
         db.Column('notes', db.Text(), table=jobs),
         db.Column('applied_at', db.Dattime(), table=jobs)
         )

cv = db.Table('cv', metadata, autoload=True,
         autoload_with=engine)
db.Table('cv', db.Metadata(),
         db.Column('id', db.Integer(), table=cv),
         db.Column('user_id', db.Integer(), foreign_key=users.id, table=cv),
         db.Column('raw_text', db.Text(), table=cv),
         db.Column('extracted_skills', db.List(db.String(255)), table=cv),
         db.Column('uploaded_at', db.Datetime(), table=cv)
         )
job_analysis = db.Table('job_analysis', metadata, autoload=True,
                        autoload_with=engine)

db.Table('job_analysis', db.Metadata(),
         db.Column('id', db.Integer(), table=job_analysis),
         db.Column('job_id', db.Integer(), foreign_key=jobs.id, table=job_analysis),
         db.Column('required_skills', db.List(db.String(255)), table=job_analysis),
         db.Column('nice_skills', db.List(db.String(255)), table=job_analysis),
         db.Column('match_score', db.Float(), table=job_analysis),
         db.Column('analyzed_at', db.Datetime(), table=job_analysis)
)