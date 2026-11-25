"""
generate_dataset.py
-------------------
Generates a sample spam/ham CSV dataset for the Email Spam Detector project.
Run this once if you do not have a real dataset:
    python dataset/generate_dataset.py
"""

import csv
import random

spam_messages = [
    "Congratulations! You have won a $1,000 gift card. Click here to claim now.",
    "FREE entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005.",
    "You are selected for a cash prize of $5000. Reply YES to claim.",
    "URGENT: Your account has been suspended. Verify now at http://fakebank.com",
    "Get paid $500 per day working from home! No experience needed.",
    "Win a brand new iPhone! Limited offer. Click the link immediately.",
    "Your loan is approved. Claim your $10,000 today. Call 1-800-FAKE.",
    "Exclusive deal! Buy 1 get 10 FREE. Only today. Click to redeem.",
    "You owe taxes. Pay immediately or face arrest. Call 1800-TAX-FAKE.",
    "Lose 20 pounds in 2 weeks! Guaranteed weight loss pill. Order now.",
    "Make money fast! Earn $1000 daily at home. No investment required.",
    "Your PayPal account is locked. Click here to unlock it immediately.",
    "Dear winner, you have been selected for a free vacation package!",
    "Cheap meds! Buy Viagra online. No prescription needed. Best price.",
    "WINNER! As a valued network customer you have been selected to receive a free prize.",
    "Claim your prize now! You have been chosen as our lucky winner today.",
    "Get rich quick! Work from home and earn $5000 weekly guaranteed.",
    "Your credit card has been charged $499. Dispute? Call 1800-SCAM.",
    "HOT SINGLES in your area! Click here to meet them tonight.",
    "Congratulations you have won FREE entry into our $250 weekly draw.",
    "ALERT! Your computer has a virus. Download our free cleaner NOW.",
    "Special offer for you! Get 90% discount on luxury brands today only.",
    "You are pre-approved for a $50,000 loan. No credit check needed.",
    "FREE ringtones! Get the latest hits on your mobile. Text RING now.",
    "Urgent message from IRS. Failure to respond may result in legal action.",
    "You've been randomly selected to win a $500 Amazon gift card!",
    "Limited time! Click here to claim your free gift before it expires.",
    "Earn passive income daily with our automated trading robot. Sign up free.",
    "Your email has won the annual lottery. Send your bank details to claim.",
    "Act now! Buy our miracle supplement and lose weight in 7 days.",
]

ham_messages = [
    "Hey, are we still meeting for lunch tomorrow at noon?",
    "Please find attached the report for the Q3 budget review.",
    "Hi, I wanted to follow up on the project proposal we discussed last week.",
    "Can you send me the meeting notes from yesterday's standup?",
    "Mom, I will be home by 7 PM. Don't worry about dinner.",
    "The team has been notified about the schedule change for Friday.",
    "I have reviewed your code and left some comments on the pull request.",
    "Looking forward to seeing you at the conference next week.",
    "Just a reminder that your library books are due back on Thursday.",
    "Thank you for your application. We will be in touch shortly.",
    "The package you ordered has been shipped. Expected delivery: 3-5 days.",
    "Please complete the feedback form by end of this week.",
    "Happy birthday! Hope you have a wonderful day.",
    "The system will be under maintenance from 2 AM to 4 AM on Sunday.",
    "Could you review the attached document and share your feedback?",
    "I wanted to check in and see how the new project is coming along.",
    "Please remember to submit your timesheet by Friday afternoon.",
    "The meeting has been rescheduled to 3 PM on Wednesday.",
    "Great work on the presentation today. The client was very impressed.",
    "Can you help me debug this Python function? I'm getting a type error.",
    "Your appointment is confirmed for Monday at 10:30 AM.",
    "The assignment is due on Friday. Please submit it via the student portal.",
    "Let me know if you need any help with the machine learning project.",
    "I am sharing the notes from today's lecture on neural networks.",
    "The semester exam timetable has been published on the university portal.",
    "Could we reschedule our call to 4 PM today instead of 3 PM?",
    "Thank you for attending the workshop. We hope you found it useful.",
    "The electricity bill for October is attached. Please review it.",
    "Reminder: Team lunch is tomorrow at 1 PM at the usual place.",
    "I have updated the shared document with the latest research findings.",
]

rows = []
for msg in spam_messages:
    rows.append({"label": "spam", "message": msg})
for msg in ham_messages:
    rows.append({"label": "ham", "message": msg})

# Duplicate and shuffle to create a larger dataset
extended = rows * 5
random.seed(42)
random.shuffle(extended)

output_path = "dataset/emails.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["label", "message"])
    writer.writeheader()
    writer.writerows(extended)

print(f"Dataset saved to {output_path} with {len(extended)} records.")
