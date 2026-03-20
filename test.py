import pyautogui
import time
import random

updates = []

actions = [
    "blinked", "looked around", "checked my phone", "scratched my head",
    "stretched", "moved my foot", "moved my other foot", "yawned",
    "sighed", "adjusted my posture", "looked at the ceiling",
    "looked at the floor", "thought about snacks", "thought about food",
    "considered standing up", "considered sitting down",
    "drank some water", "looked outside", "looked at the time",
    "opened another tab", "closed a tab", "stared into space"
]

modifiers = [
    "again", "slightly", "very slightly", "a little", "for no reason",
    "just now", "a moment ago", "without thinking", "carefully",
    "dramatically", "slowly", "quickly", "with purpose",
    "without purpose", "for safety", "just in case", "like a professional",
    "like a champion", "like a scientist", "like a potato"
]

for i in range(1000):
    action = random.choice(actions)
    modifier = random.choice(modifiers)
    updates.append(f"I {action} {modifier}.")

print("Open the Messages chat you want to send messages in.")
print("You have 5 seconds...")

time.sleep(5)

while True:
    msg = random.choice(updates)

    pyautogui.typewrite(msg)
    pyautogui.press("enter")

    print("Sent:", msg)

    time.sleep(10)