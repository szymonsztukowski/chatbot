import streamlit as st
import re
import pandas as pd
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
# Initialize session state for chat history and input if not already present
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

st.title("Classic Chatbot")

def detect_language(user_input):
    """Language detection"""
    try:
        return detect(user_input)
    except:
        return 'pl'  # Default language in case of error
    
# Form to handle both button click and pressing enter
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:", key="user_input_box")
    submit_button = st.form_submit_button("Send")


def get_response(user_input, lang='pl'):
    '''
    Function to generate a response based on user input.
    '''
    lang = detect_language(user_input) # detect language in every message

    if lang.startswith('en'):
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
        
    # polish language    
    elif lang.startswith('pl'):
        if re.search(r'żegnaj|wyjdź|zamknij', user_input, re.IGNORECASE):
            return "Dziękujemy za odwiedzenie nas. Miłego dnia!"
        elif re.search(r'pomoc|wsparcie', user_input, re.IGNORECASE):
            return "Mogę pomóc w kwestiach związanych z informacjami o produktach, śledzeniem zamówień i obsługą klienta."
        elif re.search(r'status zamówienia|śledź zamówienie', user_input, re.IGNORECASE):
            return "Podaj numer zamówienia, aby je śledzić."
        elif re.search(r'zamówienie', user_input, re.IGNORECASE):
            return "W czym mogę pomóc w związku z Twoim zamówieniem?"
        elif re.search(r'produkt', user_input, re.IGNORECASE):
            return "Którym produktem jesteś zainteresowany/a? Możesz podać nazwę lub identyfikator produktu."
        elif re.search(r'płatność|zakup|gotówka|zapłać', user_input, re.IGNORECASE):
            return "Akceptujemy wszystkie główne karty płatnicze (w tym Google Pay/Apple Pay) oraz PayPal. Możesz również wybrać opcję płatności za pobraniem."
        elif re.search(r'wysyłka|dostawa|dostawy|paczka', user_input, re.IGNORECASE):
            return "Oferujemy standardową i ekspresową wysyłkę do domu lub punktu odbioru. Podaj adres, aby sprawdzić czas dostawy i koszty."
        elif re.search(r'międzynarodowa', user_input, re.IGNORECASE):
            return "Oferujemy wysyłkę międzynarodową do większości krajów w Europie, Ameryce Północnej i Ameryce Łacińskiej. Podaj adres, aby sprawdzić czas dostawy i koszty."
        elif re.search(r'stan magazynowy|dostępność', user_input, re.IGNORECASE):
            return "Dostępność produktu jest wyświetlana na stronie produktu. Jeśli jest niedostępny, możesz zapisać się na powiadomienie o jego ponownej dostępności."
        elif re.search(r'uszkodzony', user_input, re.IGNORECASE):
            return "Przepraszamy za niedogodności. Skontaktuj się z naszym działem obsługi klienta, podając numer zamówienia i zdjęcia uszkodzonego produktu."
        elif re.search(r'gwarancja', user_input, re.IGNORECASE):
            return "Możesz zwrócić produkt w ciągu 14 dni od dostawy. Skontaktuj się z obsługą klienta, podając numer zamówienia i opis problemu, aby ubiegać się o zwrot."
        elif re.search(r'jak używać|instrukcja', user_input, re.IGNORECASE):
            return "Instrukcja obsługi jest dostępna na stronie produktu. Możesz również skontaktować się z obsługą klienta po pomoc."
        elif re.search(r'zniżki|kupony', user_input, re.IGNORECASE):
            return "Oferujemy zniżki i kupony dla nowych użytkowników oraz podczas specjalnych wydarzeń. Zapisz się do naszego newslettera, aby otrzymywać najnowsze oferty."
        elif re.search(r'usuń konto', user_input, re.IGNORECASE):
            return "Możesz usunąć swoje konto w ustawieniach konta lub skontaktować się z obsługą klienta."
        elif re.search(r'aktualizuj konto', user_input, re.IGNORECASE):
            return "Możesz zaktualizować swoje dane w ustawieniach konta."
        elif re.search(r'wypisz|anuluj subskrypcję', user_input, re.IGNORECASE):
            return "Możesz zrezygnować z subskrypcji naszego newslettera, klikając link rezygnacji na dole wiadomości e-mail."
        elif re.search(r'problem z logowaniem|zapomniane hasło', user_input, re.IGNORECASE):
            return "Możesz zresetować swoje hasło na stronie logowania lub skontaktować się z obsługą klienta po pomoc."
        elif re.search(r'promocje|wyprzedaż', user_input, re.IGNORECASE):
            return "Oferujemy promocje i wyprzedaże na nasze produkty. Sprawdź naszą stronę internetową lub zapisz się do newslettera, aby być na bieżąco."
        elif re.search(r'produkty|katalog|asortyment', user_input, re.IGNORECASE):
            return "Oferujemy szeroki wybór gier planszowych, karcianych i puzzli. Czy masz na myśli konkretny produkt?"
        elif re.search(r'zwrot|reklamacja|wymiana', user_input, re.IGNORECASE):
            return "Aby dowiedzieć się więcej o zwrotach i reklamacjach, odwiedź naszą stronę dotyczącą polityki zwrotów lub skontaktuj się z obsługą klienta."
        elif re.search(r'człowiek|konsultant|człowiekiem', user_input, re.IGNORECASE):
            return "Jestem asystentem chatbotem. Chętnie Ci pomogę! Jeśli chcesz porozmawiać z człowiekiem, skontaktuj się z naszą obsługą klienta przez e-mail lub telefon."
        else:
            return "Jestem tutaj, aby pomóc! Czy możesz sprecyzować swoje pytanie?"
    else:
        return "I can help you in English and Polish. Please type in English or Polish to get assistance."

# if submit_button and user_input:
#     # Language detection
#     try:
#         lang = detect(user_input)
#         if lang not in ['en', 'pl']: 
#             lang = 'pl'
#     except:
#         lang = 'pl'


if submit_button and user_input:
    response = get_response(user_input)
    st.session_state['chat_history'].append({"User": user_input, "Assistant": response})

# Chat history
for chat in st.session_state['chat_history']:
    st.text(f"You: {chat['User']}")
    st.text(f"Assistant: {chat['Assistant']}")
