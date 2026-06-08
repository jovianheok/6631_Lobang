# Import Python’s built-in os module to let Python interact with the operating system
import os                                                                               

# Popular Python library used to connect to and interact with a PostgreSQL database
import psycopg2                                             
                        
# Import load_env to read a .env file and load the values
from dotenv import load_dotenv                              

# Reads .env file and loads it values into os.environ
load_dotenv()

# Create and return a connection to PostgreSQL database
def get_conn():                                             
    return psycopg2.connect(os.environ["DATABASE_URL"])