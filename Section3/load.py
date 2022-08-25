import sqlite3
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from data import results

load_dotenv()

HOST = os.environ.get('HOST')
USER = os.environ.get('USER1')
PASSWORD = os.environ.get('PASSWORD')
DATABASE_NAME = 'cluster0'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
COLLECTION_NAME = 'project'
DB_FILENAME = 'project.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

client = MongoClient(MONGO_URI)
collection =client[DATABASE_NAME][COLLECTION_NAME]

# api로 받아온 데이터리스트를 MongoDB 에 저장

def insert_data(collection, list_data):

    for data in list_data:
        try :
            print(f"Inserting {data}")
            collection.insert_one(data)
        except Exception as e:
            print("Error occurred while inserting {data}")
            print(e)
insert_data(collection, results)
conn = sqlite3.connect(DB_FILENAME)
cursor = conn.cursor()
for k in collection.find():
    print(k['response']['body']['totalCount'])


#sqlite 에 테이블 생성.

#https://nfa.kspo.or.kr/front/certify/cer0303_list.do
def create_sqlite_table():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS User")

    cursor.execute(f"""CREATE TABLE User (
                        id INTEGER NOT NULL,
                        ageClass INTEGER,
                        ageDegree INTEGER,
                        aggGbn VARCHAR(20),
                        certGbn VARCHAR(20),
                        height INTEGER,
                        weight INTEGER,
                        crunch INTEGER,
                        jump INTEGER,
                        trunkFlexion FLOAT,
                        IllinoisAgility FLOAT,
                        BMI FLOAT,
                        situp INTEGER,
                        standinglongjump INTEGER,
                        standsit INTEGER,
                        twominwalk INTEGER,
                        threeMwalk INTEGER,
                        exercise VARCHAR(1000),
                        testYm VARCHAR(50),
                        PRIMARY KEY (id)
                        );""")
    cursor.close()
    conn.close()

# MongoDB 에 저장된 리스트를 SQLite 에 전달

def move_to_rdb(collection):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    for k in collection.find():
        if int(k['response']['body']['totalCount']) > 1:
            item = k['response']['body']['items']['item'] 

            for i in range(len(item)):
                cursor.execute(f"""INSERT OR IGNORE INTO User(ageClass,
                        ageDegree,
                        aggGbn,
                        certGbn,
                        height,
                        weight,
                        crunch,
                        jump,
                        trunkFlexion,
                        IllinoisAgility,
                        BMI,
                        situp,
                        standinglongjump,
                        standsit,
                        twominwalk,
                        threeMwalk,
                        exercise,
                        testYm) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (item[i]['ageClass'],
                    item[i]['ageDegree'],
                    item[i]['ageGbn'],
                    item[i]['certGbn'],
                    item[i]['itemF001'],
                    item[i]['itemF002'],
                    item[i]['itemF009'],
                    item[i]['itemF010'],
                    item[i]['itemF012'],
                    item[i]['itemF013'],
                    item[i]['itemF018'],
                    item[i]['itemF019'],
                    item[i]['itemF022'],
                    item[i]['itemF023'],
                    item[i]['itemF025'],
                    item[i]['itemF026'],
                    item[i]['presNote'],
                    item[i]['testYm']))
            conn.commit()
    cursor.close()
    conn.close()

insert_data(collection, results)
create_sqlite_table()
move_to_rdb(collection)