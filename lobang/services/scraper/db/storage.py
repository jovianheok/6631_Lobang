from db.db import get_conn                          # Import the get_conn() function from db/db.py
from psycopg2.extras import Json                    # Import the Json helper
#                                                     to convert Python dictionaries into PostgreSQL JSON format

# Save scraped posts into database
def save_raw_posts(raw_posts: list[dict], source_id: int):

    # SQL command for each post: 
#      - Insert a new row into raw_deals, with the columns and placeholders
#      - ON CONFLICT prevents duplicate inserts
#      - RETURNING id asks PostgreSQL to give back the ID of the inserted row
    sql = """INSERT INTO raw_deals (
        source_id, source_url, raw_text, raw_payload, content_hash, scraped_at)
    VALUES (%s, %s, %s, %s, %s, now())
    ON CONFLICT (source_id, content_hash) DO NOTHING
    RETURNING id;
        """
    
    inserted_ids = []                               # If a post is inserted successfully, its database ID is added to this list
    conn = get_conn()                               # Connect to PostgreSQL

    try:
        with conn:                                  # Wrap the database work in a transaction
#                                                     If everything suceed, changes are committed
#                                                     If something fails, changes are rolled back

            with conn.cursor() as cur:              # Create a cursor to run SQL commands

                for post in raw_posts:              # Loop through each post
                    cur.execute(sql,                # Run SQL query for each post
                                (source_id,
                                post["source_url"],
                                post["text"],
                                Json(post),         # Converts each Python dictionary into valid JSON text to store
                                post["content_hash"],),
                    )         
                    row = cur.fetchone()
                    if row:
                        inserted_ids.append(row[0]) # Fetch the returned row
        return inserted_ids
    
    finally:
        conn.close

def save_parsed_deals