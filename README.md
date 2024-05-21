# AWS Music Subscription Application

This project is a music subscription application developed using various AWS services. It allows users to register, login, subscribe to music, and query music based on title, artist, and year.

## Technologies Used
- AWS EC2
- AWS S3
- AWS API Gateway
- AWS Lambda
- AWS DynamoDB
- Python
- HTML/CSS/JavaScript

## Features
- User registration and login
- Music subscription management
- Music querying based on title, artist, and year
- Integration with AWS services for scalability and reliability

## Project Structure
- `music_server.py`: Backend server implemented using Flask
- `db_s3_setup.py`: Script to set up DynamoDB tables and S3 bucket
- `create_login_details.py`: Script to create login details in DynamoDB
- `index.html`: Login page HTML
- `login.css`: Login page CSS
- `register.html`: Registration page HTML
- `register.css`: Registration page CSS
- `register.js`: Registration page JavaScript
- `main.html`: Main application page HTML
- `main.css`: Main application page CSS
- `main.js`: Main application page JavaScript
- `a1.json`: Music data JSON file

## Setup and Deployment
1. Set up the necessary AWS services (EC2, S3, API Gateway, Lambda, DynamoDB).
2. Deploy the application files to the appropriate AWS services.
3. Configure the necessary permissions and settings for each service.
4. Access the application through the provided URL.

## Credits
This project was developed as part of the COSC2626/2640 Cloud Computing course at RMIT University.