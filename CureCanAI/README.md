# CureCanAI

CureCancAI is a web application built with Streamlit that helps users detect cancer. The application uses Firebase for authentication (including Google OAuth2) and features a secure signup and login system.

## Features

- **User Authentication**: Secure user signup and login with Firebase Authentication.
- **Google OAuth**: Login using Google accounts through OAuth2 integration.
- **Cancer Detection**: Leverage AI to detect cancer and present detailed results.
- **Dashboard**: Provides data visualization with beautiful charts (using libraries like Matplotlib, Plotly).
- **Responsive Design**: Streamlit provides a clean and responsive interface.

## Setup Instructions

To run the application locally, follow these steps:

### Prerequisites

- Python 3.8 or above
- Firebase account (with admin SDK setup)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/curecancai.git
   cd CureCanAI
   ```

2. **Install Dependencies:**
   ```bash
       pip install -r requirements.txt
   ```

3. **Set up environment variables:**
- Create a .env file in the root directory.
- Use the provided .env.sample as a template to add your variables

4. **Firebase Admin SDK:**
- Create a folder in the root named auth
- Add your Firebase Admin SDK JSON file under auth/ folder and update the path in your code.

5. **Run the App:**
   ```bash
   streamlit run app.py
   ```
