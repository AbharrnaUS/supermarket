import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def calculate_total_bill(bill_amount, gst_rate=18):
    return bill_amount + (bill_amount * gst_rate // 100)

def read_item_prices(prices):
    prices = {}
    try:
        with open("prices.txt", 'r') as file:
            for line in file:
                item, price = line.strip().split(',')
                prices[item] = int(price)
    except Exception as e:
        print(f"Error reading file: {e}")
    return prices

def generate_bill(items, prices):
    total = 0
    for item in items:
        if item in prices:
            total += prices[item]
        else:
            print(f"Item {item} not found in price list.")
    return total

def send_email(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    filename = 'prices.txt'
    prices = read_item_prices(filename)

    if not prices:
        print("Price list is empty or not found.")
        return

    items = []
    while True:
        item = input("Enter the item you want to add to the bill (or type 'done' to finish): ").strip()
        if item.lower() == 'done':
            break
        items.append(item)

    total_bill = generate_bill(items, prices)
    total_bill_with_gst = calculate_total_bill(total_bill)

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    bill_content = f"Bill generated on {current_datetime}\n"
    bill_content += f"Total Bill (excluding GST): {total_bill}\n"
    bill_content += f"Total Bill (including GST): {total_bill_with_gst}\n"

    print(bill_content)

    from_email = 'usabi2005@gmail.com'
    to_email = 'abharrnaus@gmail.com'
    password = 'your_password_here'  

    send_email("Your Bill", bill_content, to_email, from_email, password)

if __name__ == "_main_":
    main()
