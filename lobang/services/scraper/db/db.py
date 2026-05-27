import os                                                   # Import Python’s built-in os module
#                                                             to let Python interact with the operating system

import psycopg2                                             # Import the PostgreSQL driver
#                                                             to allow Python code to talk to a PostgreSQL database

from dotenv import load_dotenv                              # Import load_env 
#                                                             to read a .env file and load the values

load_dotenv()                                               # Reads .env file and loads it values into os.environ

# Create and return a connection to PostgreSQL database
def get_conn():                                             
    return psycopg2.connect(os.environ["DATABASE_URL"])