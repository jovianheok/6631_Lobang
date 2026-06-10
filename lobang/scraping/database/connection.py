"""
Purpose: Create a connection to our PostgreSQL database
"""

import os       # to let Python interact with the operating system                                                                       
import psycopg2     # to connect to and interact with a PostgreSQL database                                
from dotenv import load_dotenv      # to read a .env file and load the values

load_dotenv()       # Read .env file and load into os.environ

def get_conn():                                             
    return psycopg2.connect(os.environ["DATABASE_URL"])