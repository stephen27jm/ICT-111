# =====================================
#       AIRTEL MONEY MOBILE APP
# =====================================

class Node:
    def __init__(self, transaction):
        self.transaction = transaction
        self.next = None


class TransactionHistory:
    def __init__(self):
        self.head = None

    def add(self, transaction):
        new_node = Node(transaction)
        new_node.next = self.head
        self.head = new_node

    def show(self):
        current = self.head

        if current is None:
            print("No transactions yet.")
            return

        print("Your last 5 transactions:")
        count = 0

        while current is not None and count < 5:
            print(f"{count + 1}. {current.transaction['message']}")
            current = current.next
            count += 1


# REGISTERED ACCOUNTS
accounts = {
    "0777541170": {
        "password": "1234",
        "balance": 100000000.00,
        "history": TransactionHistory()
    },
    "0764107646": {
        "password": "5678",
        "balance": 100.00,
        "history": TransactionHistory()
    }
}

transfers = []
next_id = 1


# KEEP PROGRAM RUNNING
while True:
    print("\n===== AIRTEL MONEY LOGIN =====")

    while True:
        number = input("Phone Number: ")
        password = input("Password: ")

        if number in accounts and accounts[number]["password"] == password:
            print("Login successful!")
            break
        else:
            print("Incorrect phone number or password.")

    # MAIN MENU
    while True:
        user = accounts[number]

        print("\n========== MAIN MENU ==========")
        print("1. View Balance")
        print("2. Send Money")
        print("3. Deposit Money")
        print("4. Transaction History")
        print("5. Reverse Transaction")
        print("6. Withdraw Money")
        print("7. Change Password")
        print("8. Logout")

        choice = input("Choose an option: ")

        # VIEW BALANCE
        if choice == "1":
            print(f"Balance: K{user['balance']:.2f}")

        # SEND MONEY
        elif choice == "2":
            recipient = input("Recipient number: ")

            if recipient not in accounts:
                print("Recipient account not registered.")
            elif recipient == number:
                print("You cannot send money to yourself.")
            else:
                try:
                    amount = float(input("Amount to send: K"))

                    if amount <= 0:
                        print("Amount must be greater than zero.")
                    elif amount > user["balance"]:
                        print("Insufficient balance.")
                    else:
                        transfer_id = next_id
                        next_id += 1

                        transfer = {
                            "id": transfer_id,
                            "sender": number,
                            "recipient": recipient,
                            "amount": amount,
                            "reversed": False
                        }

                        user["balance"] -= amount
                        accounts[recipient]["balance"] += amount
                        transfers.append(transfer)

                        user["history"].add({
                            "message": f"Sent K{amount:.2f} to {recipient} (Ref {transfer_id})",
                            "transfer": transfer
                        })

                        accounts[recipient]["history"].add({
                            "message": f"Received K{amount:.2f} from {number} (Ref {transfer_id})",
                            "transfer": transfer
                        })

                        print("Transfer successful!")
                        print(f"Reference: {transfer_id}")
                        print(f"New balance: K{user['balance']:.2f}")

                except ValueError:
                    print("Enter a valid amount.")

        # DEPOSIT MONEY (SIMULATED)
        elif choice == "3":
            try:
                amount = float(input("Deposit amount: K"))

                if amount <= 0:
                    print("Amount must be greater than zero.")
                else:
                    user["balance"] += amount
                    user["history"].add({
                        "message": f"Deposited K{amount:.2f}",
                        "transfer": None
                    })
                    print("Deposit recorded.")
                    print(f"New balance: K{user['balance']:.2f}")

            except ValueError:
                print("Enter a valid amount.")

        # TRANSACTION HISTORY
        elif choice == "4":
            print("\n===== TRANSACTION HISTORY =====")
            user["history"].show()

        # REVERSE TRANSACTION
        elif choice == "5":
            eligible = [
                t for t in transfers
                if t["sender"] == number and not t["reversed"]
            ]

            if not eligible:
                print("No eligible sent transaction to reverse.")
            else:
                print("Your eligible sent transactions:")

                for t in eligible:
                    print(
                        f"Ref {t['id']}: K{t['amount']:.2f} "
                        f"to {t['recipient']}"
                    )

                try:
                    ref = int(input("Enter transaction reference: "))
                    transfer = next(
                        (t for t in transfers if t["id"] == ref),
                        None
                    )

                    if transfer is None or transfer["sender"] != number:
                        print("Invalid transaction reference.")
                    elif transfer["reversed"]:
                        print("This transaction was already reversed.")
                    elif accounts[transfer["recipient"]]["balance"] < transfer["amount"]:
                        print("Reversal failed: recipient has insufficient balance.")
                    else:
                        amount = transfer["amount"]
                        recipient = transfer["recipient"]

                        accounts[number]["balance"] += amount
                        accounts[recipient]["balance"] -= amount
                        transfer["reversed"] = True

                        user["history"].add({
                            "message": f"Reversal: K{amount:.2f} returned from {recipient} (Ref {ref})",
                            "transfer": None
                        })

                        accounts[recipient]["history"].add({
                            "message": f"Reversal: K{amount:.2f} returned to {number} (Ref {ref})",
                            "transfer": None
                        })

                        print("Transaction reversed successfully.")
                        print(f"New balance: K{user['balance']:.2f}")

                except ValueError:
                    print("Enter a valid reference number.")

        # WITHDRAW MONEY
        elif choice == "6":
            try:
                amount = float(input("Amount to withdraw: K"))

                if amount <= 0:
                    print("Amount must be greater than zero.")
                elif amount > user["balance"]:
                    print("Insufficient balance.")
                else:
                    user["balance"] -= amount

                    user["history"].add({
                        "message": f"Withdrew K{amount:.2f}",
                        "transfer": None
                    })

                    print("Withdrawal successful!")
                    print(f"Withdrawn: K{amount:.2f}")
                    print(f"Remaining balance: K{user['balance']:.2f}")

            except ValueError:
                print("Enter a valid amount.")

        # CHANGE PASSWORD
        elif choice == "7":
            old_password = input("Current password: ")

            if old_password == user["password"]:
                new_password = input("New password: ")
                confirm = input("Confirm new password: ")

                if new_password and new_password == confirm:
                    user["password"] = new_password
                    print("Password changed successfully.")
                else:
                    print("Passwords do not match.")
            else:
                print("Incorrect current password.")

        # LOGOUT
        elif choice == "8":
            print("Logged out successfully.")
            break

        else:
            print("Invalid option. Choose 1-8.")

    print("Returning to login page...")