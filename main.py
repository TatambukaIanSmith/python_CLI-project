import db
import members
import savings
import loans
import reports


def main():
    # Set up database tables if they don't exist yet
    db.create_tables()
    
    # Show welcome message
    print("\n" + "="*60)
    print("      WELCOME TO WARM STORMERS COMMUNITY SACCO")
    print("="*60)
    print("        Digitizing Savings for a Better Tomorrow")
    print("="*60)
    print()
    
    # Main menu loop
    while True:
        print("\n===== SACCO TRACKER MENU =====")
        print("1. Member Management")
        print("2. Savings")
        print("3. Loans")
        print("4. Reports")
        print("5. Exit")
        choice = input("Enter option: ")
        
        # Member Management section
        if choice == "1":
            print("\n--- Member Management ---")
            print("1.1 Add New Member")
            print("1.2 Search Member")
            print("1.3 View All Members")
            print("1.4 Deactivate Member")
            print("0. Back to Main Menu")
            sub = input("Enter option: ")
            
            if sub == "0":
                continue
            elif sub == "1.1" or sub == "1":
                members.add_member()
            elif sub == "1.2" or sub == "2":
                search = input("Enter name or ID: ")
                if search.isdigit():
                    m = members.find_member_by_id(int(search))
                    print(m if m else "Not found")
                else:
                    matches = members.find_member_by_name(search)
                    for m in matches:
                        print(m)
            elif sub == "1.3" or sub == "3":
                reports.print_all_members()
            elif sub == "1.4" or sub == "4":
                mid = int(input("Enter member ID: "))
                members.deactivate_member(mid)
            else:
                print("Invalid option, try again")
        
        # Savings section
        elif choice == "2":
            print("\n--- Savings ---")
            print("2.1 Record Deposit")
            print("2.2 View Member Savings")
            print("2.3 View Total SACCO Savings")
            print("0. Back to Main Menu")
            sub = input("Enter option: ")
            
            if sub == "0":
                continue
            elif sub == "2.1" or sub == "1":
                member = members.get_member_by_name_or_phone()
                if member:
                    amt = int(input("Enter deposit amount (UGX): "))
                    savings.deposit(member['id'], amt)
            elif sub == "2.2" or sub == "2":
                member = members.get_member_by_name_or_phone()
                if member:
                    total = savings.get_member_savings(member['id'])
                    print(f"Total savings for {member['name']}: UGX {total:,}")
            elif sub == "2.3" or sub == "3":
                total = savings.get_all_savings_total()
                print(f"Total SACCO savings: UGX {total:,}")
            else:
                print("Invalid option, try again")
        
        # Loans section
        elif choice == "3":
            print("\n--- Loans ---")
            print("3.1 Request Loan")
            print("3.2 Record Repayment")
            print("3.3 View Member Loans")
            print("3.4 View All Active Loans")
            print("3.5 View Overdue Loans")
            print("0. Back to Main Menu")
            sub = input("Enter option: ")
            
            if sub == "0":
                continue
            elif sub == "3.1" or sub == "1":
                member = members.get_member_by_name_or_phone()
                if member:
                    amt = int(input("Enter loan amount (UGX): "))
                    loans.request_loan(member['id'], amt)
            elif sub == "3.2" or sub == "2":
                member = members.get_member_by_name_or_phone()
                if member:
                    # Show their active loans first
                    member_loans = loans.get_member_loans(member['id'])
                    active_loans = [l for l in member_loans if l['status'] == 'active']
                    
                    if not active_loans:
                        print(f"{member['name']} has no active loans.")
                    else:
                        print(f"\n{member['name']}'s Active Loans:")
                        for loan in active_loans:
                            balance = loan['amount'] - loan['amount_repaid']
                            print(f"  Loan ID: {loan['id']} | Amount: UGX {loan['amount']:,} | Balance: UGX {balance:,}")
                        
                        lid = int(input("\nEnter loan ID to repay: "))
                        amt = int(input("Enter repayment amount (UGX): "))
                        loans.repay_loan(lid, amt)
            elif sub == "3.3" or sub == "3":
                member = members.get_member_by_name_or_phone()
                if member:
                    member_loans = loans.get_member_loans(member['id'])
                    if not member_loans:
                        print(f"No loans found for {member['name']}.")
                    else:
                        print("\n" + "="*60)
                        print(f"{member['name']}'s LOANS")
                        print("="*60)
                        for loan in member_loans:
                            balance = loan['amount'] - loan['amount_repaid']
                            print(f"Loan ID: {loan['id']}")
                            print(f"Amount: UGX {loan['amount']:,}")
                            print(f"Amount Repaid: UGX {loan['amount_repaid']:,}")
                            print(f"Balance: UGX {balance:,}")
                            print(f"Status: {loan['status'].upper()}")
                            print(f"Date Issued: {loan['date_issued']}")
                            print(f"Due Date: {loan['due_date']}")
                            print("-"*60)
            elif sub == "3.4" or sub == "4":
                reports.print_all_loans()
            elif sub == "3.5" or sub == "5":
                reports.print_overdue_loans()
            else:
                print("Invalid option, try again")
        
        # Reports section
        elif choice == "4":
            print("\n--- Reports ---")
            print("4.1 Member Statement")
            print("4.2 SACCO Summary Report")
            print("0. Back to Main Menu")
            sub = input("Enter option: ")
            
            if sub == "0":
                continue
            elif sub == "4.1" or sub == "1":
                member = members.get_member_by_name_or_phone()
                if member:
                    reports.print_member_statement(member['id'])
            elif sub == "4.2" or sub == "2":
                reports.print_sacco_summary()
            else:
                print("Invalid option, try again")
        
        # Exit
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Thank you for using Warm Stormers Community SACCO.")
        print("System exited safely.")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        print("Please contact system administrator.")
