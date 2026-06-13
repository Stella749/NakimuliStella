print("===== LOGIN SYSTEM =====")

username = input("Enter username: ")
password = input("Enter password: ")


if username == "admin":
    if password == "admin123":
        role = "Admin"
    else:
        print("Wrong password!")
        exit()

elif username == "customer":
    if password == "cust123":
        role = "Customer"
    else:
        print("Wrong password!")
        exit()

elif username == "cashier":
    if password == "cash123":
        role = "Cashier"
    else:
        print("Wrong password!")
        exit()

else:
    print("User not found!")
    exit()

print("\nLogin Successful!")
print("Welcome,", role)


if role == "Admin":
    print("Access Level: Full Access")
elif role == "Cashier":
    print("Access Level: Sales and Transactions")
else:
    print("Access Level: Shopping Only")

print("\n===== PRODUCT PURCHASE =====")

subtotal = float(input("Enter product subtotal: "))


if subtotal >= 500000:
    discount_rate = 0.15
elif subtotal >= 200000:
    discount_rate = 0.10
else:
    discount_rate = 0.05

coupon = input("Enter coupon code: ")

if coupon == "SAVE10":
    coupon_discount = 0.10
elif coupon == "SAVE20":
    coupon_discount = 0.20
else:
    coupon_discount = 0


subtotal_discount = subtotal * discount_rate
coupon_discount_amount = subtotal * coupon_discount

total_discount = subtotal_discount + coupon_discount_amount

price_after_discount = subtotal - total_discount


location = input("Enter location (Kampala, Jinja, Mbarara): ")

if location.lower() == "kampala":
    tax_rate = 0.18
elif location.lower() == "jinja":
    tax_rate = 0.15
elif location.lower() == "mbarara":
    tax_rate = 0.12
else:
    tax_rate = 0.10

tax = price_after_discount * tax_rate

final_price = price_after_discount + tax


print("\n===== RECEIPT =====")
print("Subtotal: ", subtotal)
print("Subtotal Discount: ", subtotal_discount)
print("Coupon Discount: ", coupon_discount_amount)
print("Total Discount: ", total_discount)
print("Price After Discount: ", price_after_discount)
print("Tax: ", tax)
print("Final Price: ", final_price)

print("\nThank you for shopping with us!")