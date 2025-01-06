# PhishGuardian

PhishGuardian is a Flask-based web application designed to detect and prevent phishing websites, spam emails, and spam SMS using machine learning algorithms. The application leverages a dataset sourced from Kaggle to train its models and provides a clean, intuitive interface for users.

## Features

- **URL Phishing Detection**: Detects deceptive URLs designed to trick users into divulging sensitive information or downloading malicious content.
- **Spam Email Detection**: Identifies and filters out unsolicited and potentially harmful email messages.
- **Spam SMS Detection**: Prevents unwanted and potentially malicious text messages sent to mobile devices.

## Technologies Used

- **Flask**: Backend framework for building the web application.
- **Machine Learning**: Algorithms used to analyze and classify data (e.g., phishing URLs, spam emails, spam SMS).
- **HTML/CSS**: Front-end technologies for building the user interface.
- **SQLite**: Database used to store user data and application logs.
- **Dataset**: Sourced from [Kaggle](https://www.kaggle.com/) for training the ML models.

## Installation

1. **Clone the Repository:**
   git clone https://github.com/your-username/phishguardian.git
   cd phishguardian

2. **Install Dependencies:**
pip install -r requirements.txt

3. **Run the Application:**
python app.py

The application will be available at http://127.0.0.1:5000.


## Project Structure
- **app.py**: The main Flask application file.
- **templates**: Contains the HTML templates for the application.
- **static**: Contains static files like CSS, JavaScript, and images.
- **style.css**: Custom CSS for the application's styling.
- **requirements.txt**: A file listing all the Python dependencies required by the application.
- **database.db**: SQLite database for storing user data and logs.

## Usage
Home Page
The home page welcomes users to PhishGuardian and provides an overview of the application's services. Users can navigate to different sections using the navbar.

## Services
- **URL Phishing Detection**: Users can submit URLs to check for phishing threats.
- **Spam Email Detection**: Allows users to submit emails for spam analysis.
- **Spam SMS Detection**: Provides a platform to check SMS for spam content.
- **Contact Us**: Users can reach out to the PhishGuardian team via the contact form for any queries or support.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to contribute to the project.

## Contact
For any inquiries, please contact us at support@phishguardian.com.

Note: The entire project, including the user interface and backend processing, is designed with a dark theme for a modern and sleek look. All screens in the application, including the home page, services section, and contact form, feature a black background with complementary colors for text and interactive elements.

