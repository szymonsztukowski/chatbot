import streamlit as st
import re
import pandas as pd

# Initialize session state for chat history and input if not already present
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


def get_response(user_input):
    '''
    Function to generate a response based on user input.
    '''
    if re.search(r'bye|exit|quit', user_input, re.IGNORECASE):
        return "Thank you for visiting. Have a great day!"
    elif re.search(r'help|support', user_input, re.IGNORECASE):
        return "I can assist you with product information, order tracking, and customer support."
    elif re.search(r'order status|track order', user_input, re.IGNORECASE):
        return "Please provide your order ID to track your order."
    elif re.search(r'products|catalog|items', user_input, re.IGNORECASE):
        return "We offer a wide range of products including electronics, clothing, and accessories."
    elif re.search(r'return|refund|exchange', user_input, re.IGNORECASE):
        return "For returns and refunds, please visit our return policy page or contact customer support."
    else:
        return "I'm here to help! Could you be more specific?"

# Streamlit UI
st.title("Assistant")

# Form to handle both button click and pressing enter
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:", key="user_input_box")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    response = get_response(user_input)
    st.session_state['chat_history'].append({"User": user_input, "Assistant": response})

# Chat history
for chat in st.session_state['chat_history']:
    st.text(f"You: {chat['User']}")
    st.text(f"Assistant: {chat['Assistant']}")

# Save logs to CSV file
if st.session_state['chat_history']:
    df = pd.DataFrame(st.session_state['chat_history'])
    df.to_csv("chat_logs.csv", index=False)
