import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Replace this with your own bot token
TOKEN = process.env.BOT_API
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user data
user_data = {}

# Function to handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create a reply keyboard with "Send Name and Class" button
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Send Name and Class"))
    bot.send_message(message.chat.id, "Welcome! Choose an option below:", reply_markup=markup)

# Function to handle reply keyboard button presses
@bot.message_handler(func=lambda message: message.text == "Send Name and Class")
def ask_for_name_class(message):
    # Ask the user to send their name and class
    bot.send_message(message.chat.id, "Please send your name and class in the format:\nName: John Doe\nClass: 10A")
    user_data[message.chat.id] = {"awaiting_name_class": True}  # Set flag in user data

# Function to handle name and class input
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("awaiting_name_class", False))
def handle_name_class(message):
    # Save the name and class input
    user_data[message.chat.id]["name_class"] = message.text
    user_data[message.chat.id]["awaiting_name_class"] = False  # Clear the flag

    # Update the reply keyboard to show the "Send Video" button
    bot.send_message(
        message.chat.id,
        f"Thank you! We received:\n{message.text}\n\nYou can now send your video:",
    )

# Function to handle video submissions
@bot.message_handler(content_types=['video', 'document', 'animation', 'photo'])
def handle_video(message):
    # Check if the received file is a valid video
    if message.content_type == 'video':
        # Retrieve the student's information if available
        student_info = user_data.get(message.chat.id, {}).get("name_class", "No information provided")
        
        # Confirm receipt of the video
        confirmation_message = f"Student Information:\n{student_info}\n\nVideo submitted."
        bot.send_message(message.chat.id, confirmation_message)
        
        # Forward the video to a channel (replace '@videouploadmira' with your channel username or ID)
        bot.send_video('@videouploadmira', message.video.file_id, caption=f"Video submission:\n{student_info}")
        
        # Restart the bot by invoking the /start flow
        send_welcome(message)
    else:
        # Inform the user of an invalid format
        bot.send_message(
            message.chat.id,
            "Incorrect video format! Please upload a valid video file (e.g., MP4). GIFs or other file types are not accepted."
        )

# Start polling to listen for
bot.polling()