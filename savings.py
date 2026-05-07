import db

# Record a deposit for a member
def deposit(member_id, amount):
    member = db.find_member_by_id(member_id)
    if not member:
        print("Member not found.")
        return False
    
    if not member["active"]:
        print("Member is not active.")
        return False
    
    if amount <= 0:
        print("Amount must be positive.")
        return False
    
    db.record_deposit(member_id, amount)
    print(f"✓ Deposit of UGX {amount:,} recorded for {member['name']}.")
    return True


def get_member_savings(member_id):
    return db.get_member_savings(member_id)


def get_all_savings_total():
    return db.get_all_savings_total()


def get_member_transactions(member_id):
    return db.get_member_transactions(member_id)
