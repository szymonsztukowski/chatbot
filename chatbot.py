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
    elif re.search(r'order', user_input, re.IGNORECASE):
        return "How can I assist you with your order?"
    elif re.search(r'product', user_input, re.IGNORECASE):
        return "What product are you interested in? You can type a product name or product ID."
    elif re.search(r'payment|checkout|cash|pay', user_input, re.IGNORECASE):
        return "We accept all major credit cards (including Google Pay/Apple Pay) and PayPal. You can also choose cash on delivery for your orders."
    elif re.search(r'shipping|delivery', user_input, re.IGNORECASE):
        return "We offer standard and express shipping options to your home and delivery point. Please provide your address to check the delivery time and cost."
    elif re.search(r'international', user_input, re.IGNORECASE):
        return "We offer international shipping to most countries in EU, NA, LATAM. Please provide your address to check the delivery time and cost."
    elif re.search(r'stock|item available', user_input, re.IGNORECASE):
        return "Product availability is displayed on the product page. If the product is out of stock, you can sign up for a notification when it's back."
    elif re.search(r'damaged', user_input, re.IGNORECASE):
        return "We apologize for the inconvenience. Please contact our customer support with your order ID and images of the damaged product."
    elif re.search(r'warranty', user_input, re.IGNORECASE):
        return "You can return your item up to 14 days after delivery. Please contact our customer support with your order ID and issue for refund claims."
    elif re.search(r'how do I use|how to use|', user_input, re.IGNORECASE):
        return "You can find the product manual on the product page or contact customer support for assistance."
    elif re.search(r'discounts|coupons', user_input, re.IGNORECASE):
        return "We offer discounts and coupons for new users and special events. Please subscribe to our newsletter for the latest offers."
    elif re.search(r'account delete', user_input, re.IGNORECASE):
        return "You can delete your account from the account settings page or contact customer support for assistance."
    elif re.search(r'account update', user_input, re.IGNORECASE):
        return "You can update your account information from the account settings page."
    elif re.search(r'unsubscribe', user_input, re.IGNORECASE):
        return "You can unsubscribe from our newsletter by clicking the unsubscribe link at the bottom of the email."
    elif re.search(r'trouble logging in|forgot password', user_input, re.IGNORECASE):
        return "You can reset your password from the login page or contact customer support for assistance."
    elif re.search(r'promotions|sale', user_input, re.IGNORECASE):
        return "We offer promotions and sales on our products. Please check our website or subscribe to our newsletter for the latest offers."
    elif re.search(r'products|catalog|items', user_input, re.IGNORECASE):
        return "We offer a wide range of products regarding board games, card games, and puzzles. Do you have a specific product in mind?"
    elif re.search(r'return|refund|exchange', user_input, re.IGNORECASE):
        return "For returns and refunds, please visit our return policy page or contact customer support by our e-mail address."
    elif re.search(r'human', user_input, re.IGNORECASE):
        return "I am a chatbot assistant. Feel free to ask me anything! If you're looking for a human representative, please contact our customer support by email or phone number."
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
