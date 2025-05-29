import streamlit as st
import requests
import json
import re
from langdetect import detect, DetectorFactory

# Configure language detection
DetectorFactory.seed = 0

# Configure API for the first chatbot
API_URL = st.secrets['API_URL']
API_TOKEN = st.secrets['API_TOKEN']

# Functions for the Langflow API chatbot
def call_api(user_query):
    payload = {
        "input_value": user_query,
        "output_type": "chat",
        "input_type": "chat"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=180)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error making API request: {e}"

def extract_bot_message(api_response_text):
    """
    Function to parse JSON response and extract bot message.
    Structure: outputs -> [ { outputs -> { results -> { message: { text: ... } } } } ]
    """
    try:
        data = json.loads(api_response_text)
    except json.JSONDecodeError:
        return "Error parsing API response."
    
    try:
        outputs = data.get("outputs", [])
        if outputs:
            inner_outputs = outputs[0].get("outputs", [])
            if inner_outputs:
                message_data = inner_outputs[0].get("results", {}).get("message", {})
                text = message_data.get("text")
                if text:
                    return text
    except Exception as e:
        return f"Error extracting message: {e}"
    
    return "No response content found."

# Functions for the Classic Chatbot
def detect_language(user_input):
    """Language detection"""
    try:
        return detect(user_input)
    except:
        return 'pl'  # Default language in case of error

def get_response(user_input):
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
        elif re.search(r'hej|cześć|dzień dobry', user_input, re.IGNORECASE):
            return "Cześć! Sprawy, w których mogę Ci pomóc to: wybór produktu, cena, gwarancja, zwroty, płatności, dostawa - wystarczy, że zadasz pytanie!"
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
        elif re.search(r'jakie gry|strategiczne|planszowe|polecacie', user_input, re.IGNORECASE):
            return "Polecamy następujące gry strategiczne z naszej oferty: Scythe - rozbudowana strategia z kontrolą terytorium, ekonomią i walką. \n Twilight Imperium - epicka gra kosmiczna z polityką, eksploracją i bitewnością. \n Nemesis: Lockdown - asymetryczna gra z ukrytymi celami i napięciem."
        elif re.search(r'jakie gry rodzinne|gry rodzinne', user_input, re.IGNORECASE):
            return "Oto kilka polecanych gier dla rodzin z naszej oferty: Dixit – kreatywna i pięknie ilustrowana gra skojarzeń. \n Wsiąść do Pociągu: Europa – łatwa do nauczenia, idealna dla dzieci i dorosłych. \n Catan – klasyk o handlu i budowie z prostymi zasadami. \n  Monopoly – znana gra ekonomiczna dla całej rodziny. \n Everdell – bajkowy świat z prostym worker placementem, który dzieci też zrozumieją."
        elif re.search(r'jakie gry ekonomiczne|gry euro', user_input, re.IGNORECASE):
            return "Polecamy te gry z naszej oferty oparte na planowaniu, zarządzaniu i małej losowości: Ark Nova – duża strategia ekonomiczna z planowaniem kart. \n Iki – klasyczne euro z interesującym mechanizmem ruchu po planszy. \n Catan – prostsza gra ekonomiczna z handlem i budową."
        elif re.search(r'scythe|Scythe', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 299 zł. \n Gra strategiczna osadzona w alternatywnej Europie, łącząca ekonomię, kontrolę terytorium i rozwój frakcji. Gracze wykonują akcje: produkcja, ruch, walka i budowa."
        elif re.search(r'Catan|Catan', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 149 zł. \n Gracze zbierają surowce, budują drogi, osady i miasta. Celem jest zdobycie 10 punktów zwycięstwa. Istotną rolę odgrywa handel między graczami."
        elif re.search(r'dixit|Dixit', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 129 zł. \n Gracze opowiadają skojarzenia do ilustracji na kartach, a inni próbują odgadnąć, o którą kartę chodzi. Gra opiera się na wyobraźni i kreatywności."
        elif re.search(r'Monopoly|monopoly', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 109 zł. \n Gracze kupują i rozwijają nieruchomości, pobierają czynsze i dążą do bankructwa przeciwników. Zwycięża ostatni gracz, który nie zbankrutował."
        elif re.search(r'everdell|Everdell', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 229 zł. \n Gra typu worker placement i budowanie tableau. Gracze zarządzają zasobami, wystawiają budynki i postacie, rozwijając swoje leśne miasto."
        elif re.search(r'wsiąść do pociągu|europa|Europa|Wsiąść do pociągu', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 179 zł. \n Gracze zbierają karty wagonów i budują połączenia kolejowe między miastami Europy. Punkty zdobywa się za długość tras i realizację biletów."
        elif re.search(r'Nemesis: Lockdown|nemesis|lockdown|Nemesis', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 379 zł. \n Semi-kooperacyjna gra sci-fi z ukrytymi celami. Gracze eksplorują bazę na Marsie, walczą z obcymi i próbują przetrwać. Możliwa zdrada graczy."
        elif re.search(r'Ark Nova|ark nova', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 269 zł. \n Gracze projektują nowoczesne zoo. Gra oparta na kartach, zarządzaniu projektami, sponsorami i zwierzętami. Cel to zdobycie jak największej reputacji i dobrostanu."
        elif re.search(r'Iki|iki', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 179 zł. \n Gra euro osadzona w japońskim Edo. Gracze zatrudniają rzemieślników, planują zakupy na targu i rozwijają swoją reputację. Ważne jest zarządzanie ruchem po planszy."
        elif re.search(r'Twilight Imperium|Twilight', user_input, re.IGNORECASE):
            return "Cena w naszym sklepie: 699 zł. \n Epicka gra strategiczna 4X. Gracze budują imperia, eksplorują kosmos, prowadzą wojny i głosują nad prawami. Gra pełna polityki i negocjacji – trwa wiele godzin."
        else:
            return "Jestem tutaj, aby pomóc! Czy możesz sprecyzować swoje pytanie?"
    else:
        return "I can help you in English and Polish. Please type in English or Polish to get assistance."

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# App layout
st.title("Projekt licencjacki - chatboty")
st.write("Zadaj pytanie poniżej!")

# Display conversation history
for message in st.session_state.conversation_history:
    st.markdown(f"**Ty**: {message['user']}")
    
    # Display both bot responses in columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Chatbot 1")
        st.markdown(f"{message['langflow_bot']}")
    with col2:
        st.markdown("### Chatbot 2")
        st.markdown(f"{message['classic_bot']}")
    
    st.markdown("---")

# Input form
with st.form(key='unified_chat_form', clear_on_submit=True):
    user_input = st.text_input("Twoje pytanie:", key="user_input_field")
    submit_button = st.form_submit_button("Wyślij")

# Process the form submission
if submit_button and user_input:
    # Get responses from both chatbots
    
    # First chatbot (Langflow API)
    api_response_text = call_api(user_input)
    if api_response_text.startswith("Error"):
        langflow_response = api_response_text
    else:
        langflow_response = extract_bot_message(api_response_text)
    
    # Second chatbot (Classic rule-based)
    classic_response = get_response(user_input)
    
    # Save messages to conversation history
    st.session_state.conversation_history.append({
        "user": user_input,
        "langflow_bot": langflow_response,
        "classic_bot": classic_response
    })
    
    # Use st.rerun() instead of the deprecated experimental_rerun
    st.rerun()