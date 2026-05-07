import db

# Helper function to add new members to the SACCO
def add_member():
    # Get and validate name
    while True:
        name = input("Enter member name: ").strip()
        
        if not name:
            print("Please enter a proper name with letters.")
            continue
        
        # Make sure it's not just numbers
        if name.replace(" ", "").isdigit():
            print("Please enter a proper name with letters.")
            continue
        
        # Only letters and spaces allowed
        if not all(c.isalpha() or c.isspace() for c in name):
            print("Please enter a proper name with letters.")
            continue
        
        if not any(c.isalpha() for c in name):
            print("Please enter a proper name with letters.")
            continue
        
        break
    
    # To get the phone number
    while True:
        phone = input("Enter phone number: ").strip()
        if len(phone) != 10 or not phone.isdigit():
            print("Invalid phone number. Must be exactly 10 digits.")
            continue
        
        # Check if someone already has this number
        all_members = db.get_all_members()
        phone_exists = False
        for m in all_members:
            if m['phone'] == phone:
                print(f"Phone number already registered to {m['name']} (ID: {m['id']}).")
                phone_exists = True
                break
        
        if phone_exists:
            continue

        break
    
    # All good, let's add them
    member_id = db.add_member(name, phone)
    print(f"✓ Member added. ID: {member_id}")
    print(f"✓ {name} can now use their name and phone number for transactions.")
    return member_id


def find_member_by_id(member_id):
    return db.find_member_by_id(member_id)


def find_member_by_name(name):
    return db.find_member_by_name(name)


# This function helps find members by name, and if there are duplicates,
# it asks for the phone number to identify the right person
def get_member_by_name_or_phone():
    name = input("Enter member name: ")
    matches = db.find_member_by_name(name)
    
    if not matches:
        print("No member found with that name.")
        return None
    
    if len(matches) == 1:
        member = matches[0]
        print(f"✓ Found: {member['name']} (ID: {member['id']}, Phone: {member['phone']})")
        return member
    
    # multiple people with the same name
    print(f"\nFound {len(matches)} members with that name:")
    for m in matches:
        print(f"- {m['name']} (Phone: {m['phone']})")
    
    # Asking for phone to identify the right one
    phone = input("\nEnter phone number to identify the correct member: ")
    for m in matches:
        if m['phone'] == phone:
            print(f"✓ Found: {m['name']} (ID: {m['id']})")
            return m
    
    print("No member found with that phone number.")
    return None


def deactivate_member(member_id):
    member = find_member_by_id(member_id)
    if member:
        db.deactivate_member(member_id)
        print(f"✓ Member {member['name']} deactivated.")
    else:
        print("Member not found.")
