import mysql.connector
from Server.Properties import INSERT_QUERY, DB_PASSWORD, DB_USER, DB_NAME, DB_HOST,\
    DB_ERR_MSG

#Establishes connection with MySql with MySql DB_HOST
def getDBConnection():
    db = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                              host=DB_HOST,
                              database=DB_NAME)
    return db;


def insertClientStats(data):
    try:
        db=getDBConnection();                              
        cur=db.cursor()
        cur.execute(INSERT_QUERY,(data['username'],data["timestamp"],data["hostname"],data["IPAddress"],data["CPUCount"],data["CPUUsage"],data["MemoryUsage"],data["Uptime"]));
        db.commit()
        db.close()
    except Exception as e:
        print(DB_ERR_MSG,e)