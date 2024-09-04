import smtplib, ssl, csv, random
from email.message import EmailMessage

replyto = 'Your Reply-to Email Id'
subject = 'Request to Schedule Interview for DevOps and Cloud Opening'
name = 'Dilip Kumar IIIT VADODARA'

counter = {}

with open("user.csv") as f:
    data = [row for row in csv.reader(f)]

# Single email template file
file_list = ['emails/message1.txt']

resume_link = "https://drive.google.com/file/d/1RC1pXpOf4eFgyt4y5yHU_MMHYzG573ri/view?usp=sharing"
# Email message content to be added
email_content = f"""
Dear Sir/Madam,

I hope this message finds you well. I wanted to follow up on my application for the DevOps Cloud role at Your Company. I’m very excited about the opportunity and would like to schedule an interview at your earliest convenience.

Please let me know a suitable time, and I will adjust my schedule accordingly.

Thank you for considering my application. I look forward to your response.

You can find my resume here: {resume_link}

Best regards,
Dilip Kumar
7857089254
"""

# Send emails
with open('mails.csv', 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        # Skip empty rows
        if not row or len(row) < 1:
            continue
        
        random_user = random.choice(data)
        sender = random_user[0]
        password = random_user[1]
        
        if sender not in counter:
            counter[sender] = 0
        
        if counter[sender] >= 500:
            continue
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(sender, password)
                em = EmailMessage()
                em['From'] = f'{name} <{sender}>'
                em['Reply-To'] = replyto
                em['To'] = row[0]
                em['Subject'] = subject
                
                # Combine email template with the provided content
                email_body = email_content
                em.set_content(email_body)

                # Send the email
                server.send_message(em)
                counter[sender] += 1
                print(counter[sender], " emails sent", "From ", sender, "To ", row[0])

                # Update mails.csv to remove the sent row
                with open("mails.csv", "r") as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                rows = rows[1:]
                if rows:
                    with open("mails.csv", "w", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)

        except Exception as e:
            print(f"Error sending email From {sender} to {row[0]}:", e)
            with open("mails.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
                rows = rows[1:]
            if rows:
                with open("mails.csv", "w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

# Final report of emails sent
print("Emails Sent")
for sender, count in counter.items():
    print(f"{sender}: {count}")
