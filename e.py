import sqlite3
import forgery_py
import faker
import random
import names
import math
import datetime

def create_accounts_table(conn):
    """
    Creates the 'accounts' table in the given database connection.

    Args:
        conn: A sqlite3 connection object.
    """
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS accounts (
                    Account_ID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    creditonhold INTEGER NOT NULL,
                    Followemail BOOLEAN NOT NULL,
                    describtion TEXT NOT NULL,
                    Address TEXT NOT NULL
                )""")
    conn.commit()

def create_leads_table(conn):
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS leads (
                    Lead_ID INTEGER PRIMARY KEY,
                    Account_ID INTEGER NOT NULL,
                    Date_Generated DATETIME NOT NULL,
                    Email TEXT NOT NULL,
                    FOREIGN KEY (Account_ID) REFERENCES accounts (Account_ID)
                )""")
    conn.commit()

def create_opportunities_table(conn):
    """
    Creates the 'opportunities' table in the given database connection.

    Args:
        conn: A sqlite3 connection object.
    """
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS opportunities (
                    Opportunity_ID INTEGER PRIMARY KEY,
                    Account_ID INTEGER NOT NULL,
                    FOREIGN KEY (Account_ID) REFERENCES accounts (Account_ID),
                    Date_created DATETIME NOT NULL,
                    Converted_from INTEGER,
                    FOREIGN KEY (Converted_from) REFERENCES leads (Lead_ID),
                    Opportunity_Size INTEGER NOT NULL
                )""")
    conn.commit()

def create_interactions_table(conn):
    """
    Creates the 'interactions' table in the given database connection.

    Args:
        conn: A sqlite3 connection object.
    """
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS interactions (
                    Interaction_ID INTEGER PRIMARY KEY,
                    Account_ID INTEGER NOT NULL,
                    FOREIGN KEY (Account_ID) REFERENCES accounts (Account_ID),
                    Date DATETIME NOT NULL,
                    Description TEXT NOT NULL
                )""")
    conn.commit()
def create_orders_table(conn):
    """
    Creates the 'orders' table in the given database connection.

    Args:
        conn: A sqlite3 connection object.
    """
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS orders (
                    Order_ID INTEGER PRIMARY KEY,
                    Account_ID INTEGER NOT NULL,
                    FOREIGN KEY (Account_ID) REFERENCES accounts (Account_ID),
                    Date DATETIME NOT NULL,
                    Amount REAL NOT NULL
                )""")
    conn.commit()

def drop_all_tables(conn):
    """
    Drops all tables in the given database connection.

    Args:
        conn: A sqlite3 connection object.
    """
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS accounts")
    c.execute("DROP TABLE IF EXISTS leads")
    c.execute("DROP TABLE IF EXISTS opportunities")
    c.execute("DROP TABLE IF EXISTS interactions")
    c.execute("DROP TABLE IF EXISTS orders")
    conn.commit()
def create_random_accounts(conn, num_accounts):
    """
    Generates and inserts random accounts into the 'accounts' table in the given database connection.

    Args:
        conn: A sqlite3 connection object.
        num_accounts: The number of random accounts to generate.
    """
    c = conn.cursor()
    fake = faker.Faker()

    for i in range(num_accounts):
        name = forgery_py.name.company_name()
        creditonhold = random.randint(0, 100)
        followemail = random.choice([True, False])
        describtion = "This is a random description for a company."
        address = fake.street_address() + ", " + fake.city()

        c.execute("INSERT INTO accounts (Name, creditonhold, Followemail, describtion, Address) VALUES (?, ?, ?, ?, ?)", (name, creditonhold, followemail, describtion, address))
    conn.commit()

def sin_curve(x, amplitude, frequency, phase):
    """Calculates a sin curve with the given parameters.

    Args:
        x (float): The x value to calculate the sin curve for.
        amplitude (float): The amplitude of the sin curve.
        frequency (float): The frequency of the sin curve.
        phase (float): The phase of the sin curve.

    Returns:
        float: The y value of the sin curve for the given x value.
    """
    return amplitude * math.sin(x * frequency) + phase


def create_random_leads(conn, init_date, days, a, b, c):
    """
    Creates random leads using a sin curve to determine the number of leads generated each day.

    Args:
        conn (sqlite3.Connection): The connection to the database.
        init_date (datetime.datetime): The starting date for generating leads.
        days (int): The number of days to generate leads for.
        a (float): The amplitude of the sin curve.
        b (float): The frequency of the sin curve.
        c (float): The phase of the sin curve.
    """
    c = conn.cursor()
    fake = faker.Faker()

    # Iterate over the number of days
    for i in range(days):
        # Calculate the number of leads to generate for this day using the sin curve
        num_leads = round(100*sin_curve(1, 2, 3, 2))

        # Generate the leads
        for j in range(num_leads):
            # Select a random account to associate the lead with
            accounts = c.execute("SELECT * FROM accounts").fetchall()
            account = random.choice(accounts)

            # Generate the lead data
            date_generated = init_date + datetime.timedelta(days=i)
            email = fake.email()
            lead_id = i * num_leads + j + 1  # Generate a unique lead_id

            # Insert the lead into the database
            c.execute("INSERT INTO leads (Lead_ID, Account_ID, Date_Generated, Email) VALUES (?, ?, ?, ?)", (lead_id, account[0], date_generated, email))

    # Save the changes to the database
    conn.commit()








# Connect to the database
conn = sqlite3.connect("crm.db")

drop_all_tables(conn)

# Create the tables in the database
create_accounts_table(conn)
create_leads_table(conn)
#create_opportunities_table(conn)
#create_interactions_table(conn)
#create_orders_table(conn)

# Generate 100 random accounts and insert them into the 'accounts' table
create_random_accounts(conn, 100)

# Set the starting date and number of days for generating leads
init_date = datetime.datetime.now()
days = 365

# Generate leads using a sin curve with the specified parameters
create_random_leads(conn, init_date, days, 3, 1, 3)

# Generate 200 random opportunities and insert them into the 'opportunities' table
#create_random_opportunities(conn, init_date, days, 200)

# Generate interactions and orders for the accounts and insert them into the respective tables
#create_random_interactions_and_orders(conn, init_date, days)

# Close the database connection
conn.close()
