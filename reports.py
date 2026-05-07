import db
from datetime import date


def print_all_members():
    print("=" * 50)
    print("ALL MEMBERS")
    print("=" * 50)
    for m in db.get_all_members():
        status = "Active" if m["active"] else "Inactive"
        print(f"ID: {m['id']} | {m['name']} | {m['phone']} | {status}")
    print("=" * 50)


def print_member_statement(member_id):
    print("=" * 50)
    print("MEMBER STATEMENT")
    print("=" * 50)
    member = db.find_member_by_id(member_id)
    if not member:
        print("Member not found.")
        print("=" * 50)
        return
    print(f"Name: {member['name']}")
    print(f"Phone: {member['phone']}")
    print(f"Joined: {member['joined']}")
    total_savings = db.get_member_savings(member_id)
    print(f"Total Savings: UGX {total_savings:,}")
    for loan in db.get_member_loans(member_id):
        print(f"Loan: UGX {loan['amount']:,} | Repaid: UGX {loan['amount_repaid']:,} | Status: {loan['status']}")
    print("=" * 50)


def print_all_loans():
    print("=" * 70)
    print("ALL ACTIVE LOANS")
    print("=" * 70)
    loans = db.get_all_loans()
    active_loans = [loan for loan in loans if loan["status"] == "active"]
    
    if not active_loans:
        print("No active loans at the moment.")
        print("All members have either cleared their loans or no loans have been issued.")
    else:
        print(f"Total Active Loans: {len(active_loans)}\n")
        for loan in active_loans:
            member = db.find_member_by_id(loan['member_id'])
            balance = loan["amount"] - loan["amount_repaid"]
            print(f"Loan ID: {loan['id']}")
            print(f"Member: {member['name']} (ID: {member['id']}, Phone: {member['phone']})")
            print(f"Loan Amount: UGX {loan['amount']:,}")
            print(f"Amount Repaid: UGX {loan['amount_repaid']:,}")
            print(f"Balance: UGX {balance:,}")
            print(f"Date Issued: {loan['date_issued']}")
            print(f"Due Date: {loan['due_date']}")
            print("-" * 70)
    print("=" * 70)


def print_sacco_summary():
    print("=" * 35)
    print("SACCO SUMMARY REPORT")
    print("=" * 35)
    members = db.get_all_members()
    total_members = len(members)
    active_members = sum(1 for m in members if m["active"])
    total_savings = db.get_all_savings_total()
    loans = db.get_all_loans()
    total_loans = sum(l["amount"] for l in loans)
    total_repaid = sum(l["amount_repaid"] for l in loans)
    print(f"Total Members      : {total_members}")
    print(f"Active Members     : {active_members}")
    print(f"Total Savings      : UGX {total_savings:,}")
    print(f"Total Loans Issued : UGX {total_loans:,}")
    print(f"Total Repaid       : UGX {total_repaid:,}")
    print(f"Outstanding Loans  : UGX {total_loans - total_repaid:,}")
    print("=" * 35)


def print_overdue_loans():
    print("=" * 70)
    print("OVERDUE LOANS")
    print("=" * 70)
    today = date.today()
    found = False
    for loan in db.get_all_loans():
        if loan["status"] != "cleared":
            due = loan["due_date"]
            if isinstance(due, str):
                import datetime
                due = datetime.date.fromisoformat(due)
            if today > due:
                member = db.find_member_by_id(loan['member_id'])
                balance = loan["amount"] - loan["amount_repaid"]
                days_overdue = (today - due).days
                print(f"Loan ID: {loan['id']}")
                print(f"Member: {member['name']} (Phone: {member['phone']})")
                print(f"Loan Amount: UGX {loan['amount']:,}")
                print(f"Balance: UGX {balance:,}")
                print(f"Due Date: {loan['due_date']}")
                print(f"Days Overdue: {days_overdue} days")
                print("-" * 70)
                found = True
    if not found:
        print("No overdue loans. All loans are up to date!")
    print("=" * 70)