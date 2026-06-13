print("=== World Cup 2026 Simulator ===")
print("Type 'exit' to quit the program.")
print("Type 'secret' to see a hidden feature.")
print("-" * 35)

while True:
    country = input("\nEnter a country to see if they will win World Cup 2026: ").strip().lower()
    
    if country == 'exit':
        print("Exiting the simulator. Thanks for playing!")
        break
        
    if country == 'secret':
        pass 
        print("The 'pass' statement executed! (This is just a placeholder block).")
        continue

    if country == "":
        print("You didn't enter anything. Please try again.")
        continue
        
    if country == 'argentina' or country == 'brazil' or country == 'france':
        print(f"High probability! {country.title()} has a massive chance to win World Cup 2026!")
    elif country == 'usa' or country == 'mexico' or country == 'canada':
        print(f"Host advantage! {country.upper()} might pull off a historic miracle!")
    else:
        print(f"{country.title()} will put up a great fight, but 2026 might not be their year.")