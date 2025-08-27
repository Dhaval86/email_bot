import streamlit as st
import smtplib
import ssl
from email.message import EmailMessage
import os
import pandas as pd

# Set page title
st.set_page_config(page_title="Email Sender Chatbot", layout="centered")
st.title("📧 Email Sender Chatbot")

# Chatbot instructions
st.write("Upload an Excel file, enter recipient email, and I'll help you send it as an attachment.")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# Input recipient email
recipient_email = st.text_input("Enter recipient email address")

# Input subject and message
subject = st.text_input("Email Subject", value="Here is the Excel file you requested")
body = st.text_area("Email Body", value="Please find the attached Excel file.")

# Sender credentials (You can store these securely in environment variables)
sender_email = st.text_input("Your Email Address")
password = st.text_input("Your Email Password (use app password for Gmail)", type="password")

# Validate uploaded file
if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")
    df = pd.read_excel(uploaded_file)
    st.write("Preview of your Excel file:")
    st.dataframe(df)

# Send email when user clicks button
if st.button("Send Email"):
    if not uploaded_file:
        st.error("Please upload an Excel file.")
    elif not recipient_email:
        st.error("Please enter the recipient email.")
    elif not sender_email or not password:
        st.error("Please enter your email and password.")
    else:
        try:
            # Save file temporarily
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Create email
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg.set_content(body)

            # Attach file
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_name = uploaded_file.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

            # Send email via SMTP (Gmail example)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg)

            st.success(f"✅ Email sent successfully to {recipient_email}!")
            os.remove(file_path)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# import streamlit as st
# import smtplib
# import ssl
# from email.message import EmailMessage
# import os
# import pandas as pd

# # Configure Streamlit page
# st.set_page_config(page_title="Email Sender Chatbot", layout="centered")
# st.title("💬 Email Sender Chatbot")

# # Initialize session state for conversation flow
# if 'step' not in st.session_state:
#     st.session_state.step = 0
# if 'uploaded_file' not in st.session_state:
#     st.session_state.uploaded_file = None
# if 'recipient_email' not in st.session_state:
#     st.session_state.recipient_email = ""
# if 'subject' not in st.session_state:
#     st.session_state.subject = ""
# if 'body' not in st.session_state:
#     st.session_state.body = ""
# if 'sender_email' not in st.session_state:
#     st.session_state.sender_email = ""
# if 'password' not in st.session_state:
#     st.session_state.password = ""

# # Chatbot flow
# if st.session_state.step == 0:
#     st.write("👋 Hi! Please upload the Excel file you want to send.")
#     uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
#     if uploaded_file is not None:
#         st.session_state.uploaded_file = uploaded_file
#         st.session_state.step = 1
#     st.warning("Please manually refresh the page to see updates.")

# elif st.session_state.step == 1:
#     st.success("✅ File uploaded successfully!")
#     df = pd.read_excel(st.session_state.uploaded_file)
#     st.write("Here's a quick preview of your file:")
#     st.dataframe(df)
#     st.write("Please provide the recipient's email address:")
#     recipient_email = st.text_input("Recipient Email", key="recipient_email_input")
#     if recipient_email:
#         st.session_state.recipient_email = recipient_email
#         st.session_state.step = 2
#     st.warning("Please manually refresh the page to see updates.")

# elif st.session_state.step == 2:
#     st.write(f"Recipient Email: **{st.session_state.recipient_email}**")
#     st.write("Now enter the email subject and message:")
#     subject = st.text_input("Subject", value="Here is the Excel file you requested")
#     body = st.text_area("Email Body", value="Please find the attached Excel file.")
#     if subject and body:
#         st.session_state.subject = subject
#         st.session_state.body = body
#         st.session_state.step = 3
#     st.warning("Please manually refresh the page to see updates.")

# elif st.session_state.step == 3:
#     st.write("Great! Now enter your email credentials:")
#     sender_email = st.text_input("Your Email Address")
#     password = st.text_input("Your Email Password (use app password for Gmail)", type="password")
#     if sender_email and password:
#         st.session_state.sender_email = sender_email
#         st.session_state.password = password
#         st.session_state.step = 4
#     st.warning("Please manually refresh the page to see updates.")

# elif st.session_state.step == 4:
#     st.write("✅ All details collected! Here is a summary:")
#     st.write(f"- **Recipient:** {st.session_state.recipient_email}")
#     st.write(f"- **Subject:** {st.session_state.subject}")
#     st.write(f"- **Message:** {st.session_state.body}")
#     st.write(f"- **File:** {st.session_state.uploaded_file.name}")

#     if st.button("Send Email"):
#         try:
#             # Save uploaded file temporarily
#             file_path = os.path.join(os.getcwd(), st.session_state.uploaded_file.name)
#             with open(file_path, "wb") as f:
#                 f.write(st.session_state.uploaded_file.getbuffer())

#             # Create email
#             msg = EmailMessage()
#             msg['Subject'] = st.session_state.subject
#             msg['From'] = st.session_state.sender_email
#             msg['To'] = st.session_state.recipient_email
#             msg.set_content(st.session_state.body)

#             # Attach file
#             with open(file_path, "rb") as f:
#                 file_data = f.read()
#                 file_name = st.session_state.uploaded_file.name
#             msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

#             # Send email via SMTP (Gmail example)
#             context = ssl.create_default_context()
#             with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
#                 server.login(st.session_state.sender_email, st.session_state.password)
#                 server.send_message(msg)

#             st.success(f"✅ Email sent successfully to {st.session_state.recipient_email}!")
#             os.remove(file_path)

#         except Exception as e:
#             st.error(f"❌ Error: {str(e)}")
