import db
from datetime import date
import savings


def check_loan_eligibility(member_id):
    member_savings = savings.get_member_savings(member_id)
    max_loan = member_savings * 3  # Can borrow up to 3x their savings
    has_active = db.get_active_loan_count(member_id) > 0
    return max_loan, has_active


def request_loan(member_id, amount):
    member = db.find_member_by_id(member_id)
    if not member:
        print("Member not found.")
        return False
    
    if not member["active"]:
        print("Member is not active.")
        return False
    max_loan, has_active = check_loan_eligibility(member_id)
    
    if has_active:
        print("Member already has an active loan.")
        return False
    
    if amount > max_loan:
        print(f"Member savings: UGX {savings.get_member_savings(member_id):,} | Max loan: UGX {max_loan:,}")
        print("Loan amount exceeds eligibility.")
        return False
    
    if amount <= 0:
        print("Amount must be positive.")
        return False
    
    # Calculate due date (3 months from today)
    today = date.today()
    due_year = today.year
    due_month = today.month + 3
    if due_month > 12:
        due_month -= 12
        due_year += 1
    due_date = date(due_year, due_month, today.day)
    
    db.add_loan(member_id, amount, due_date)
    print(f"✓ Loan of UGX {amount:,} approved. Due: {due_date}")
    return True


def repay_loan(loan_id, amount):
    if amount <= 0:
        print("Amount must be positive.")
        return False
    
    try:
        loan = db.repay_loan(loan_id, amount)
        if loan:
            balance = loan['amount'] - loan['amount_repaid']
            print(f"✓ Repayment of UGX {amount:,} recorded.")
            print(f"Total repaid: UGX {loan['amount_repaid']:,}")
            print(f"Balance remaining: UGX {balance:,}")
            print(f"Status: {loan['status'].upper()}")
            if loan['status'] == 'cleared':
                print("Loan fully paid!")
        else:
            print("Error: Loan not found.")
        return True
    except Exception as e:
        print(f"Error processing repayment: {e}")
        return False


def get_loan_balance(loan_id):
    return db.get_loan_balance(loan_id)


def get_member_loans(member_id):
    return db.get_member_loans(member_id)
