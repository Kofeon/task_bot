import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id INT,
    name TEXT,
    is_creator BOOL,
    dollar_balance FLOAT,
    wallet_address TEXT,
    refs INT,
    invited INT
    )
''')

cur.execute('''CREATE TABLE IF NOT EXISTS telegram_channel_tasks (
    task_id INT,
    channel INT,
    creator_id INT,
    type TEXT,
    quantity INT,
    executed_quantity INT, 
    price FLOAT,
    time TEXT,
    who_did TEXT
    )
''')

cur.execute('''CREATE TABLE IF NOT EXISTS another_tasks (
    task_id INT,
    proof_type TEXT,
    text TEXT,
    quantity INT,
    executed_quantity INT,
    price FLOAT,
    who_did TEXT
    )
''')

con.commit()