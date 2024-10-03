import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

def add_custom_css():
    st.markdown("""
        <style>
        /* Background color */
        body {
            background-color: #1e1e1e;
            color: #dcdcdc;
        }
        /* Text input styles */
        input {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #444444;
            padding: 8px;
        }
        /* Header styles */
        h1, h2, h3, h4, h5, h6 {
            color: #d4af37; /* Gold-like color for headers */
        }
        /* Subheader style */
        .stMarkdown h2 {
            font-size: 1.8em;
            color: #ffcc00; /* Yellowish color */
        }
        /* Button style */
        div.stButton button {
            background-color: #008CBA;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-size: 1em;
            transition: background-color 0.3s ease;
        }
        div.stButton button:hover {
            background-color: #005f7a;
        }
        /* Balloons style */
        .balloon-container {
            background-color: #1e1e1e;
        }
        /* Selectbox style */
        select {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #444444;
        }
        </style>
    """, unsafe_allow_html=True)

if not firebase_admin._apps:
    cred = credentials.Certificate("auth\curecanai-c2ca277ea96b.json")
    firebase_admin.initialize_app(cred)

st.title("CureCancAI - Account Page")

add_custom_css()

def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        if user:
            st.session_state['username'] = user.uid
            st.session_state['useremail'] = user.email
            st.session_state['logged_in'] = True
        else:
            st.error("Invalid login credentials")
    except Exception as e:
        st.error(f"Login failed: {e}")

# Function to handle signup
def signup(username, email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            uid=username
        )
        st.session_state['username'] = username
        st.session_state['useremail'] = email
        st.session_state['logged_in'] = True
        st.balloons()
        st.success("Signup successful")
    except Exception as e:
        st.error(f"Signup failed: {e}")

def logout():
    st.session_state.clear()

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.markdown("<h2 style='color: #d4af37;'>Welcome to your account</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #dcdcdc; font-size: 1.2em;'>Username: <strong style='color: #ffcc00;'>{st.session_state['username']}</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #dcdcdc; font-size: 1.2em;'>Email: <strong style='color: #ffcc00;'>{st.session_state['useremail']}</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #dcdcdc; font-size: 1.2em;'>You have successfully logged in or signed up.</p>", unsafe_allow_html=True)
    
    if st.button("Sign Out"):
        logout()

else:
    login_signup_choice = st.selectbox("Choose an option", ["Login", "Sign Up"])

    if login_signup_choice == "Login":
        st.subheader("Login to your account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(email, password)
    elif login_signup_choice == "Sign Up":
        st.subheader("Create a new account")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            signup(username, email, password)
