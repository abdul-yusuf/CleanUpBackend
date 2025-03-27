<H1>CLEANUP BACKEND</H1><BR>
Cleanup is a mobile app designed to help users manage and recycle waste effectively. The app offers several key features such as:
<UL>
<LI>Learning Phase: Provides educational content on waste management, teaching users how to separate, manage, and recycle waste. It also explains how users can earn money by selling recyclable materials.</LI>
<LI>⁠Waste Scan: An AI-powered tool that scans waste to identify types (e.g., plastic, paper, metal, etc.) and provides recommendations on whether users can recycle the waste locally or need to contact a vendor for proper disposal.</LI>
<LI>⁠Marketplace: Connects users with local vendors who purchase waste. Users can input the type and quantity of waste, see vendor prices, and arrange pickups or sales.</LI>
</UL>

# Django Project Setup Guide

This guide will help you clone and set up this Django project on your local machine.

## **1. Prerequisites**
Ensure you have the following installed on your system:
- **Python (3.10)
- **Git**
- **pip (Python package manager)**

## **2. Clone the Repository**
```sh
git clone https://github.com/abdul-yusuf/CleanUpBackend.git
```
## **3. Create a Virtual Environment**
It's best to install dependencies in an isolated environment:
```sh
python -m venv venv
```
Activate the virtual environment:

Windows (Git Bash)
```sh
source venv/Scripts/activate
```

Mac/Linux
```sh
source venv/bin/activate
```

## **4. Install Dependencies**
```sh
pip install -r requirements.txt
```

## **6. Apply Migrations**
```sh
python manage.py migrate
```

## **7. Create a Superuser**
`For accessing admin panel:

```sh
python manage.py createsuperuser
```

## **8. Run the Server**
```sh
python manage.py runserver
```
