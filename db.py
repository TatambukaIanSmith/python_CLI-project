import pymysql
from datetime import date

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="python_db",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()


def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(15),
            joined DATE,
            active BOOLEAN DEFAULT TRUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS savings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            member_id INT,
            amount INT,
            date DATE,
            recorded_by VARCHAR(50)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            member_id INT,
            amount INT,
            date_issued DATE,
            due_date DATE,
            amount_repaid INT DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active'
        )
    """)
    connection.commit()


def add_member(name, phone):
    joined = date.today()
    cursor.execute("INSERT INTO members (name, phone, joined) VALUES (%s, %s, %s)", (name, phone, joined))
    connection.commit()
    return cursor.lastrowid


def find_member_by_id(member_id):
    cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
    return cursor.fetchone()


def find_member_by_name(name):
    cursor.execute("SELECT * FROM members WHERE name LIKE %s", (f"%{name}%",))
    return cursor.fetchall()


def deactivate_member(member_id):
    cursor.execute("UPDATE members SET active = FALSE WHERE id = %s", (member_id,))
    connection.commit()


def record_deposit(member_id, amount):
    today = date.today()
    cursor.execute("INSERT INTO savings (member_id, amount, date, recorded_by) VALUES (%s, %s, %s, %s)", (member_id, amount, today, "Treasurer"))
    connection.commit()
    return cursor.lastrowid


def get_member_savings(member_id):
    cursor.execute("SELECT SUM(amount) as total FROM savings WHERE member_id = %s", (member_id,))
    result = cursor.fetchone()
    if result and result["total"]:
        return result["total"]
    return 0


def get_all_savings_total():
    cursor.execute("SELECT SUM(amount) as total FROM savings")
    result = cursor.fetchone()
    if result and result["total"]:
        return result["total"]
    return 0


def get_member_transactions(member_id):
    cursor.execute("SELECT * FROM savings WHERE member_id = %s", (member_id,))
    return cursor.fetchall()


def add_loan(member_id, amount, due_date):
    today = date.today()
    cursor.execute("INSERT INTO loans (member_id, amount, date_issued, due_date) VALUES (%s, %s, %s, %s)", (member_id, amount, today, due_date))
    connection.commit()
    return cursor.lastrowid


def repay_loan(loan_id, amount):
    cursor.execute("UPDATE loans SET amount_repaid = amount_repaid + %s WHERE id = %s", (amount, loan_id))
    connection.commit()
    cursor.execute("SELECT * FROM loans WHERE id = %s", (loan_id,))
    loan = cursor.fetchone()
    if loan and loan["amount_repaid"] >= loan["amount"]:
        cursor.execute("UPDATE loans SET status = 'cleared' WHERE id = %s", (loan_id,))
        connection.commit()
        cursor.execute("SELECT * FROM loans WHERE id = %s", (loan_id,))
        loan = cursor.fetchone()
    return loan


def get_loan_balance(loan_id):
    cursor.execute("SELECT amount, amount_repaid FROM loans WHERE id = %s", (loan_id,))
    loan = cursor.fetchone()
    if loan:
        return loan["amount"] - loan["amount_repaid"]
    return None


def get_member_loans(member_id):
    cursor.execute("SELECT * FROM loans WHERE member_id = %s", (member_id,))
    return cursor.fetchall()

def get_active_loan_count(member_id):
    cursor.execute("SELECT COUNT(*) as cnt FROM loans WHERE member_id = %s AND status = 'active'", (member_id,))
    result = cursor.fetchone()
    return result["cnt"] if result else 0


def get_loan(loan_id):
    cursor.execute("SELECT * FROM loans WHERE id = %s", (loan_id,))
    return cursor.fetchone()


def get_all_members():
    cursor.execute("SELECT * FROM members")
    return cursor.fetchall()


def get_all_loans():
    cursor.execute("SELECT * FROM loans")
    return cursor.fetchall()


def get_all_savings():
    cursor.execute("SELECT * FROM savings")
    return cursor.fetchall()