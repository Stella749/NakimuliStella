bill = float(input("Enter total bill amount: "))
while bill <= 0:
    print("Bill amount must be greater than 0.")
    bill = float(input("Enter total bill amount: "))

people = int(input("Enter number of people: "))
while people <= 0:
    print("Number of people must be greater than 0.")
    people = int(input("Enter number of people: "))

tip_percent = float(input("Enter tip percentage: "))
while tip_percent < 0:
    print("Tip percentage cannot be negative.")
    tip_percent = float(input("Enter tip percentage: "))
    
tip_amount = bill * (tip_percent / 100)
total_bill = bill + tip_amount
amount_per_person = total_bill / people

# Output
print("\n===== BILL RECEIPT =====")
print(f"Bill Amount:      {bill:.2f}")
print(f"Tip Percentage:   {tip_percent}%")
print(f"Tip Amount:       {tip_amount:.2f}")
print(f"Total Bill:       {total_bill:.2f}")
print(f"Number of People: {people}")
print(f"Amount Per Person:{amount_per_person:.2f}")
print("========================")