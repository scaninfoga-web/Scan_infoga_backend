import os
import django
import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # Replace with your project name
django.setup()

from hudsonrock.models import HudsonRockData  # Replace with your app name

# Sample data
sample_data = {
    "stealer": "RedLine",
    "stealerFamily": "RedLine Stealer",
    "dateUploaded": datetime.datetime(2024, 4, 1, 12, 0),
    "employeeAt": ["CompanyA", "CompanyB"],
    "clientAt": ["ClientX"],
    "dateCompromised": datetime.datetime(2024, 3, 25, 10, 30),
    "ip": "192.168.1.100",
    "computerName": "USER-PC",
    "operatingSystem": "Windows 10 Pro",
    "malwarePath": "C:\\Users\\user\\AppData\\Local\\Temp\\malware.exe",
    "antiviruses": ["Windows Defender", "Malwarebytes"],
    "credentials": [
        {
            "url": "https://example.com",
            "domain": "example.com",
            "username": "john_doe",
            "password": "password123",
            "type": "web"
        },
        {
            "url": "https://gmail.com",
            "domain": "gmail.com",
            "username": "john.doe@gmail.com",
            "password": "securepass!",
            "type": "email"
        }
    ],
    "data_type": "email"
}

# Create and save to DB
record = HudsonRockData(**sample_data)
record.save()

print("Sample HudsonRockData record inserted successfully.")
