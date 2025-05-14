import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Set page config
st.set_page_config(page_title="User Portal", page_icon=":rocket:", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
        main {
            overflow: auto; /* Enable scrolling */
            width: 100vw; /* Set viewport width */
            height: 100vh; /* Set viewport height */
            white-space: nowrap; /* Prevent wrapping */
        }
        /* Ensure columns and content don't wrap */
        block-container {
            display: flex; 
            flex-wrap: nowrap; /* Disable wrapping */
        }
        stApp {
            background-color: #E0F7FA;
        }
        header {
            background-color: #0288D1;
            color: white;
            padding: 15px 0;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            border-radius: 5px;
        }
        footer {
            background-color: #0288D1;
            color: white;
            padding: 8px;
            text-align: center;
            position: fixed;
            width: 90%;
            bottom: 0;
            font-size: 16px;
            border-radius: 5px;
        }
        h1, h2, h3 {
            text-align: center;
            color: #01579B;
        }
        label, .stTextInput>label, .stNumberInput>label, .stSelectbox>label {
            font-weight: bold;
            color: #01579B;
            font-size: 18px;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: #ffffff;
            border: 2px solid #0288D1;
            border-radius: 8px;
            padding: 5px;
            font-size: 20px;
            color: #000000;
        }
        .stButton {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .custom-label {
        font-size: 20px; /* Adjust font size */
        font-weight: bold; /* Optional: Make it bold */
        color: #00000; /* Optional: Change text color */
        margin-bottom: 0px; /* Reduce spacing below the label */
        }
        .stButton>button {
            background-color: #0288D1;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 20px 50px;
            font-size: 40px;
        }
        .stButton>button:hover {
            background-color: #0277BD;
        }

        /* Change background color */
        .stApp {
                background-color: #f5f5f5; /* Light gray */
        }
                    
        /* Table styling */
        .scrollable-table {
                max-height: 800px;
                overflow-y: auto;
                border: 1px solid #ddd;
                width: 100%;
        }
        .styled-table {
            border-collapse: collapse;
            width: 100%;
            font-size: 14px;
            text-align: left;
            background-color: #FFFFFF; /* Light gray background */
        }
        .styled-table th, .styled-table td {
            border: 1px solid #000000;
            padding: 8px;
            white-space: nowrap; /* Prevent text wrapping */
        }
        .styled-table th {
            background-color: #009879;
            color: white;
        }
        
                
        /* Custom form styling */
        .stForm {
            background-color: #ADD8E6; /* Light blue */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .form-header {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333333; /* Dark gray */
        }
        .custom-label {
            font-size: 20px;
            margin-bottom: 0px;
            color: #333333; /* Dark gray */
        }
        /* Radio button styling */
        .stRadio > label {
            font-size: 25px; /* Larger text */
            font-weight: bold;
        }
        .stRadio div[role="radio"] {
            transform: scale(10); /* Increase button size */
            margin-right: 15px; /* Space between buttons */
        }

        .stButton > button {
            background-color: #1E90FF !important; /* Dodger blue */
            color: white !important;
            font-size: 24px !important;
            padding: 30px 40px !important;
            border-radius: 8px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #0059b3 !important; /* Darker blue on hover */
        }
        .stForm button {
            background-color: #FFD700 !important; /* Dodger blue */
            color: black !important;
            font-size: 24px !important; /* Larger button text */
            padding: 20px 30px !important; /* Increased button size */
            border-radius: 8px;
            border: none;
            font-weight: bold;
        }
        .stForm button:hover {
            background-color: #DAA520 !important; /* Darker blue on hover */
        }
        .styled-table td, .styled-table th {
            border: 2px solid #0288D1 !important;
            text-align: center !important;
            padding: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)


# Files for storing data
CUSTOMER_DATA_FILE = 'customer_data.json'
USER_INPUT_DATA_FILE = 'user_input_data.csv'

# Helper functions
def load_customer_data():
    try:
        with open(CUSTOMER_DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}

def save_customer_data(data):
    with open(CUSTOMER_DATA_FILE, 'w') as file:
        json.dump(data, file)

def load_user_input_data():
    try:
        return pd.read_csv(USER_INPUT_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Name", "Address", "Number", "Marka", "Date"])

def save_user_input_data(df):
    df.to_csv(USER_INPUT_DATA_FILE, index=False)

def forgot_password_page():
    st.header("Reset Your Password")

    # Initialize session state for verification
    if "is_verified" not in st.session_state:
        st.session_state.is_verified = False
    if "reset_username" not in st.session_state:
        st.session_state.reset_username = ""

    if not st.session_state.is_verified:
        username = st.text_input("Enter your username")
        phone = st.text_input("Enter your registered phone number")

        if st.button("Verify"):
            customer_data = load_customer_data()

            if username in customer_data and customer_data[username].get("number") == phone:
                st.success("Verified. Please set your new password.")
                st.session_state.is_verified = True
                st.session_state.reset_username = username
                st.rerun()  # Force rerun to show password fields
            else:
                st.error("Username and phone number do not match.")

    else:
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")

        if st.button("Reset Password"):
            if new_pass == confirm_pass and new_pass.strip() != "":
                customer_data = load_customer_data()
                customer_data[st.session_state.reset_username]["password"] = new_pass
                save_customer_data(customer_data)
                st.success("Password reset successfully. Go to login.")

                # Clear session state
                st.session_state.is_verified = False
                st.session_state.reset_username = ""
                st.session_state.page = "Login"
                st.rerun()
            else:
                st.error("Passwords do not match or are empty.")


def render_styled_table(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d-%b-%Y")

    def row_style(row):
        if row.get("Action") == "Update":
            return "background-color: #c8e6c9;"  # light green
        elif row.get("Action") == "Delete":
            return "background-color: #ffcdd2;"  # light red
        return ""

    html = """
    <style>
    .custom-table-container {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        text-align: center;
    }
    th {
        background-color: #00796B;
        color: white;
        border: 2px solid #0288D1;
        padding: 10px;
        text-align: center;
        font-size: 16px;
    }
    td {
        border: 2px solid #0288D1;
        padding: 8px;
        text-align: center;
        font-size: 15px;
    }
    </style>
    <div class="custom-table-container">
    <table>
        <thead>
            <tr>""" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += f"<tr style='{row_style(row)}'>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"

    html += "</tbody></table></div>"

    st.markdown(html, unsafe_allow_html=True)
def render_styled_table_1(df):
    df = df.copy()
    df["registration_time"] = pd.to_datetime(df["registration_time"], errors="coerce").dt.strftime("%d-%b-%Y")

    def row_style(row):
        if row.get("Action") == "Update":
            return "background-color: #c8e6c9;"  # light green
        elif row.get("Action") == "Delete":
            return "background-color: #ffcdd2;"  # light red
        return ""

    html = """
    <style>
    .custom-table-container {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        text-align: center;
    }
    th {
        background-color: #00796B;
        color: white;
        border: 2px solid #0288D1;
        padding: 10px;
        text-align: center;
        font-size: 16px;
    }
    td {
        border: 2px solid #0288D1;
        padding: 8px;
        text-align: center;
        font-size: 15px;
    }
    </style>
    <div class="custom-table-container">
    <table>
        <thead>
            <tr>""" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += f"<tr style='{row_style(row)}'>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"

    html += "</tbody></table></div>"

    st.markdown(html, unsafe_allow_html=True)

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Registration page
def register_customer():
    st.header("Register New User")
    col1, col2, col3 = st.columns(3)

    # Section 1 (Left Column)
    with col2:
        st.markdown('<div class="custom-label">Choose Username:</div>', unsafe_allow_html=True)
        username = st.text_input('')
        st.markdown('<div class="custom-label">Choose Password:</div>', unsafe_allow_html=True)
        password = st.text_input('', type="password")
        st.markdown('<div class="custom-label">Full Name:</div>', unsafe_allow_html=True)
        name = st.text_input('',key='name')
        st.markdown('<div class="custom-label">Address:</div>', unsafe_allow_html=True)
        address = st.text_input('',key='address')
        st.markdown('<div class="custom-label">Phone Number:</div>', unsafe_allow_html=True)
        number = st.text_input('',key='number')

    if st.button("Register"):
        if username == "" or password == "" or name == "":
            st.error("Please fill all required fields.")
            return

        customer_data = load_customer_data()

        if username in customer_data:
            st.error("Username already exists!")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            customer_data[username] = {
                "password": password,
                "name": name,
                "address": address,
                "number": number,
                "registration_time": current_time
            }
            save_customer_data(customer_data)
            st.success("Registration successful! Redirecting to login page...")
            st.session_state.page = "Login"
            st.rerun()


# Login page
def login_page():
    st.header("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_clicked = st.button("Login")

    if login_clicked:
        customer_data = load_customer_data()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.success("Admin login successful")
            st.session_state['logged_in_user'] = 'admin'
        elif username in customer_data:
            user_info = customer_data[username]
            if user_info.get("password") == password:
                st.success(f"User login successful: {username}")
                st.session_state['logged_in_user'] = username
            else:
                st.error("Incorrect password.")
        else:
            st.error("User not found. Please register.")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("New user? Register here"):
            st.session_state.page = "Register"
            st.rerun()
    with col3:
        if st.button("Forgot Password?"):
            st.session_state.page = "ForgotPassword"
            st.rerun()
# User dashboard
def user_dashboard(username):
    st.header(f"Welcome {username}! Submit Your Information")
    col1, col2, col3 = st.columns(3)
    df = load_user_input_data()
    with col2:
        st.markdown('<div class="custom-label">Name:</div>', unsafe_allow_html=True)
        name = st.text_input("",key='login_name')
        st.markdown('<div class="custom-label">Number:</div>', unsafe_allow_html=True)
        number = st.text_input("",key='login_number')
        st.markdown('<div class="custom-label">Address:</div>', unsafe_allow_html=True)
        address = st.text_input("",key='login_add')
        st.markdown('<div class="custom-label">Marka:</div>', unsafe_allow_html=True)
        marka = st.text_input("",key='login_marka')

    if st.button("Submit Data"):
        new_data = pd.DataFrame([{
            "Username": username,
            "Name": name,
            "Address": address,
            "Number": number,
            "Marka": marka,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        save_user_input_data(df)
        st.success("Data submitted successfully!")

    st.subheader("Your Submitted Data")
    user_data = df[df['Username'] == username]
    user_data.insert(0, "ID", user_data.index)

    if not user_data.empty:
        render_styled_table(user_data)

        if "show_edit_controls" not in st.session_state:
            st.session_state.show_edit_controls = False

        if not st.session_state.show_edit_controls:
            if st.button("Click here to Update or Delete your data"):
                st.session_state.show_edit_controls = True
                st.rerun()
        else:
            selected_index = st.selectbox("Select row to update/delete (by index)", user_data.index.tolist())
            action = st.selectbox("Action", ["Update", "Delete"])

            # Define background color
            action_color = {
                "Update": "#c8e6c9",  # light green
                "Delete": "#ffcdd2"   # light red
            }
            selected_color = action_color.get(action, "#ffffff")

            # Show colored box
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color:{selected_color}; padding: 10px; border-radius: 10px;">
                        <label style="font-weight:bold;">Selected Row Index:</label><br>
                        <div>{selected_index}</div>
                        <br>
                        <label style="font-weight:bold;">Selected Action:</label><br>
                        <div>{action}</div>
                    </div>
                    """, unsafe_allow_html=True
                )

            if action == "Update":
                co1, co2, co3 = st.columns(3)
                with co2:
                    st.markdown('<div class="custom-label">Update Name:</div>', unsafe_allow_html=True)
                    updated_name = st.text_input("", value=user_data.loc[selected_index, 'Name'], key='Update name')
                    st.markdown('<div class="custom-label">Update Address:</div>', unsafe_allow_html=True)
                    updated_address = st.text_input("", value=user_data.loc[selected_index, 'Address'], key="Update address")
                    st.markdown('<div class="custom-label">Update Number:</div>', unsafe_allow_html=True)
                    updated_number = st.text_input("", value=user_data.loc[selected_index, 'Number'], key="Update number")
                    st.markdown('<div class="custom-label">Update Marka:</div>', unsafe_allow_html=True)
                    updated_marka = st.text_input("", value=user_data.loc[selected_index, 'Marka'], key='Update Marka')

                if st.button("Update Now"):
                    df.loc[selected_index, 'Name'] = updated_name
                    df.loc[selected_index, 'Address'] = updated_address
                    df.loc[selected_index, 'Number'] = updated_number
                    df.loc[selected_index, 'Marka'] = updated_marka
                    save_user_input_data(df)
                    st.success("Updated Successfully!")
                    st.rerun()

            if action == "Delete":
                if st.button("Delete Now"):
                    df = df.drop(index=selected_index)
                    save_user_input_data(df)
                    st.success("Deleted Successfully!")
                    st.rerun()
    else:
        st.info("No data submitted yet.")

# Admin dashboard
def admin_dashboard():
    st.header("Admin Dashboard")

    customer_data = load_customer_data()
    user_input_data = load_user_input_data()

    tab1, tab2 = st.tabs(["Registered Users", "User Inputs"])

    with tab1:
        st.subheader("All Registered Users")
        if customer_data:
            df_customer = pd.DataFrame.from_dict(customer_data, orient='index')
            render_styled_table_1(df_customer)

            st.download_button(
                label="Download Registered Users Data",
                data=df_customer.to_csv(index=True),
                file_name="registered_users.csv",
                mime='text/csv'
            )
        else:
            st.info("No registered users found.")

    with tab2:
        st.subheader("All User Inputs")

        try:
            if not user_input_data.empty:
                # Convert Date column
                user_input_data['Date'] = pd.to_datetime(user_input_data['Date'], errors='coerce')

                min_date = user_input_data['Date'].min().date()
                max_date = user_input_data['Date'].max().date()

                date_selection = st.date_input("Select Date or Date Range", (min_date, max_date))

                # Handle single date and range
                if isinstance(date_selection, tuple):
                    start_date, end_date = date_selection
                else:
                    start_date = end_date = date_selection

                # Filter data safely
                filtered_data = user_input_data[
                    (user_input_data['Date'].dt.date >= start_date) &
                    (user_input_data['Date'].dt.date <= end_date)
                    ]

                # Styling: center text and shade header


                render_styled_table(filtered_data)

                if not filtered_data.empty:
                    filename = f"user_inputs_{start_date}_to_{end_date}.csv" if start_date != end_date else f"user_inputs_{start_date}.csv"
                    st.download_button(
                        label="Download Filtered User Input Data",
                        data=filtered_data.to_csv(index=False),
                        file_name=filename,
                        mime='text/csv'
                    )
                else:
                    st.info("No data found for the selected date(s).")
            else:
                st.info("No user inputs found.")
        except Exception as e:
            st.error(f"Please Select Particular Date Range Or Select That Specific Day Once for Getting Result")


# Main app flow
def main():
    st.markdown('<header>My Company Portal</header>', unsafe_allow_html=True)

    if 'logged_in_user' not in st.session_state:
        st.session_state['logged_in_user'] = None
    if 'page' not in st.session_state:
        st.session_state['page'] = "Login"
    if st.session_state.page == "ForgotPassword":
        forgot_password_page()

    # Logged in user view
    if st.session_state['logged_in_user']:
        if st.session_state['logged_in_user'] == 'admin':
            admin_dashboard()
        else:
            user_dashboard(st.session_state['logged_in_user'])
    else:
        # Page selection based on session state
        if st.session_state.page == "Login":
            login_page()
        elif st.session_state.page == "Register":
            register_customer()


    st.markdown('<footer>© 2025 My Company Pvt. Ltd.</footer>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
