import psycopg2
import pandas as pd
from sqlalchemy import create_engine,text
import json
import os
from dotenv import load_dotenv
load_dotenv()


host= os.getenv('host')
db=os.getenv('db')
username=os.getenv('db_username')
user = username
dbname=db
password=os.getenv('password')
port=os.getenv('port')


def create_connection(application_name="LearnystDjangoData"):
    
    print("Establising connection with database")
    
    conn = psycopg2.connect(
    database=db , user=username, password= password, host=host , port= port,application_name = application_name
    )
    
    print("Connection established with database")
    

    return conn

conn = create_connection()

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}")


def processquery(query: str,application_name:str="",args={}) -> pd.DataFrame:
    global conn
    
    # conn = psycopg2.connect(
    # database=db , user=username, password= password, host=host , port= port
    # )

    """returns the query as pandas dataframe from database
    Args:
    --------
        query (str): query
    
    Returns:
    ---------
        data: pandas dataframe from query
    """
    
    if conn.closed != 0:
        conn = create_connection()      
            
    table = pd.read_sql(query, con=conn,params=args)
      
    
    return table

def excute_query(query:str,args={},application_name:str=""):
    
    global conn
    
    try:
        if conn.closed != 0:
            conn = create_connection()
        cursor = conn.cursor()   
        
        cursor.execute(query=query,vars=args)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise Exception(e)
    
  
    
def excute_query_and_return_data_one(query:str,application_name:str=""):
    data = ()
    
    global conn
    
    try:
        
        if conn.closed != 0:
            conn = create_connection()
        cursor = conn.cursor()   
        
        cursor.execute(query=query)
                
        
        data = cursor.fetchone()[0]

        return data
    
    except Exception as e:
        print(e)
        conn.close()
        raise Exception(e)
        
    

def excute_query_and_return_data(query:str,application_name:str=""):
    data = ()
    
    global conn
    
    try:
        if conn.closed != 0:
            conn = create_connection()
            
        cursor = conn.cursor()  
              
        cursor.execute(query=query)
        
        
        data = cursor.fetchone()
    except Exception as e:
        conn.close()
        raise Exception(e)

    
    return data

def excute_query_and_return_data_all(query:str,application_name:str=""):
    data = ()
    
    global conn
    
    try:
        if conn.closed != 0:
            conn = create_connection()
        cursor = conn.cursor()   
     
        cursor.execute(query=query)
        
        data = cursor.fetchall()
        
    except Exception as e:
        conn.close()
        raise Exception(e)
    
    
    return data