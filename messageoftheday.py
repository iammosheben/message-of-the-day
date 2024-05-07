import os
import requests
import random
import time
import wikipedia
import randfacts
from bs4 import BeautifulSoup
from datetime import datetime
from ShynaJokes import ShynaJokes
from twilio.rest import Client
from tinydb import TinyDB, Query
from deep_translator import GoogleTranslator
import subscription  # Import the subscription module

# Twilio account credentials
account_sid = 'ACd73b9b2cf303706bf7adacc8806eea5d'
auth_token = '506e814351b774aca809f4f64866849a'
twilio_whatsapp_number = 'whatsapp:+14155238886'

# Imgur Client ID
imgur_client_id = '72b55fa928fc2f1'

# Initialize Twilio Client
client = Client(account_sid, auth_token)

# Initialize ShynaJokes
shyna_jokes = ShynaJokes.ShynaJokes()

# Fetch a random fact from the randfacts package
def get_random_useless_fact():
    try:
        fact = randfacts.get_fact()
        return fact
    except Exception as e:
        return f"Error fetching random fact: {e}"

# Fetch a random fact from Interesting Facts API (API Ninjas)
def get_random_interesting_fact():
    try:
        response = requests.get(
            "https://api.api-ninjas.com/v1/facts",
            headers={"X-Api-Key": "your_api_ninjas_key"},
            params={"limit": 1}
        )
        if response.status_code == 200 and response.json():
            return response.json()[0]["fact"]
        else:
            return "Unable to fetch interesting fact from API Ninjas."
    except Exception as e:
        return f"Error fetching interesting fact from API Ninjas: {e}"

# Fetch historical events by scraping Wikipedia's "On This Day" page
def get_today_in_history_wikipedia_scrape():
    try:
        today = datetime.today()
        month = today.strftime("%B")
        day = today.day
        url = f"https://en.wikipedia.org/wiki/{month}_{day}"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        events_section = soup.find(id="Events")

        if events_section:
            ul = events_section.find_next("ul")
            events = [li.text.strip() for li in ul.find_all("li")]
            today_events = random.sample(events, min(2, len(events)))
            return "\n".join(today_events)
        else:
            return "Unable to find historical events."
    except Exception as e:
        return f"Error fetching historical events: {e}"

# Fetch a random animal fact from some-random-api
def get_random_animal_fact_some_random_api():
    try:
        animal_list = ["dog", "cat", "panda", "raccoon", "kangaroo", "fox", "bird", "koala", "red_panda"]
        animal = random.choice(animal_list)
        response = requests.get(f"https://some-random-api.ml/animal/{animal}")
        if response.status_code == 200 and response.json():
            data = response.json()
            return f"{animal.capitalize()}: {data['fact']}"
        else:
            return "Unable to fetch animal fact from some-random-api."
    except Exception as e:
        return f"Error fetching animal fact from some-random-api: {e}"

# Fetch a random summary from a Wikipedia article
def get_random_wikipedia_summary():
    max_retries = 3
    for i in range(max_retries):
        try:
            wikipedia.set_lang("en")
            random_title = wikipedia.random()
            summary = wikipedia.summary(random_title, sentences=2)
            return f"{random_title}\n{summary}"
        except Exception as e:
            if i == max_retries - 1:
                return f"Error fetching random Wikipedia summary: {e}"

# Fetch a joke of the day from ShynaJokes with fallback
def get_joke_of_the_day():
    try:
        joke = shyna_jokes.shyna_pun_joke()
        return joke
    except Exception as e:
        return f"Why don't some couples go to the gym? Because some relationships don't work out."

# Download Bing Picture of the Day and save it locally
def download_bing_picture_of_the_day(image_directory="images"):
    try:
        response = requests.get(
            "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
        )
        if response.status_code == 200 and response.json():
            data = response.json()["images"][0]
            title = data.get("title", "Bing Picture of the Day")
            description = data.get("copyright", "No description available")
            url = f"https://www.bing.com{data['url']}"

            # Download the image
            image_data = requests.get(url).content

            # Create the images directory if it doesn't exist
            os.makedirs(image_directory, exist_ok=True)

            # Define the local file path
            image_filename = os.path.join(image_directory, "bing_picture_of_the_day.jpg")

            # Save the image locally
            with open(image_filename, "wb") as image_file:
                image_file.write(image_data)

            return image_filename, f"{title}\nDescription: {description}"
        else:
            return None, "Unable to fetch Bing Picture of the Day."
    except Exception as e:
        return None, f"Error fetching Bing Picture of the Day: {e}"

# Upload an image to Imgur and return the direct image URL
def upload_image_to_imgur(image_path, max_retries=3, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            headers = {
                "Authorization": f"Client-ID {imgur_client_id}"
            }
            files = {"image": (os.path.basename(image_path), open(image_path, "rb"), "image/jpeg")}
            response = requests.post(
                "https://api.imgur.com/3/upload",
                headers=headers,
                files=files
            )
            if response.status_code == 200 and response.json():
                imgur_data = response.json()["data"]
                # Ensure the direct URL points to `.jpeg`
                direct_img_url = imgur_data["link"].replace("https://imgur.com/", "https://i.imgur.com/") + ".jpeg"
                print(f"Imgur Direct URL: {direct_img_url}")
                return direct_img_url
            else:
                print(f"Error uploading to Imgur: {response.status_code}, {response.text}")
                retries += 1
                time.sleep(retry_delay)
        except Exception as e:
            print(f"Exception uploading to Imgur: {e}")
            retries += 1
            time.sleep(retry_delay)
    
    print("Max retries exceeded. Unable to upload image to Imgur.")
    return None

# Consolidate interesting and useless facts
def get_combined_interesting_fact():
   useless_fact = get_random_useless_fact()
   interesting_fact = get_random_interesting_fact()

   if "Unable to fetch" not in interesting_fact:
       return f"{useless_fact}\n\n{interesting_fact}"
   else:
       return useless_fact

# Create a comprehensive message containing all facts
def get_comprehensive_message(recipient_name, language):
   combined_fact = get_combined_interesting_fact()
   today_in_history = get_today_in_history_wikipedia_scrape()
   animal_fact = get_random_animal_fact_some_random_api()
   wikipedia_summary = get_random_wikipedia_summary()
   joke_of_the_day = get_joke_of_the_day()
   bing_image_path, bing_description = download_bing_picture_of_the_day()

   # Combine all into a single message with bold titles
   message = (
       f"*Hello {recipient_name}! Here's your Message of the Day:*\n\n"
       "*🖼️ Picture of the Day:*\n"
       f"{bing_description}\n\n"
       "*💡 Interesting Facts:*\n"
       f"{combined_fact}\n\n"
       "*📜 Today in History:*\n"
       f"{today_in_history}\n\n"
       "*🐾 Animal Facts:*\n"
       f"{animal_fact}\n\n"
       "*📖 Random Wikipedia Summary:*\n"
       f"{wikipedia_summary}\n\n"
       "*😂 Joke of the Day:*\n"
       f"{joke_of_the_day}\n\n"
       "*Enjoy your day and keep learning!*"
   )

   # Translate the message if a language other than English is specified
   if language != "en":
       translator = GoogleTranslator(target=language)
       message = translator.translate(message)

   return message, bing_image_path

# Send a comprehensive message to a WhatsApp number using Twilio
def send_whatsapp_message_with_image(recipient_number, message, image_path):
   imgur_url = upload_image_to_imgur(image_path)
   if imgur_url:
       try:
           media_message = client.messages.create(
               from_=twilio_whatsapp_number,
               body=message,
               media_url=[imgur_url],
               to=recipient_number
           )
           print(f"Message sent successfully with SID: {media_message.sid}")
       except Exception as e:
           print(f"Error sending message: {e}")
   else:
       print("Error uploading image to Imgur.")

# Function to send the message to all subscribers
# Function to send the message to all subscribers
# Function to send the message to all subscribers
def send_message_to_subscribers():
    db = TinyDB('subscribers.json')
    subscribers = db.all()
    for subscriber in subscribers:
        recipient_number = subscriber['phone_number']
        recipient_name = subscriber['name']
        language = subscriber['language']

        message, bing_image_path = get_comprehensive_message(recipient_name, language)
        send_whatsapp_message_with_image(recipient_number, message, bing_image_path)

# Main function to send the message to all subscribers
def main():
   send_message_to_subscribers()

if __name__ == '__main__':
   main()