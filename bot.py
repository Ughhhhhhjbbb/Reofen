from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Define a function to handle messages
def chat_with_gpt(update, context):
    user_message = update.message.text
    try:
        # Use OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": user_message}]
        )
        # Send the response back to the user
        update.message.reply_text(response["choices"][0]["message"]["content"])
    except Exception as e:
        update.message.reply_text("An error occurred: " + str(e))

# Start the bot
def main():
    # Set up the Telegram bot with your bot token
    updater = Updater("6528857056:AAEf72nHTZ4xbK7viLuUSVdYRtuIbVLldmc", use_context=True)
    dp = updater.dispatcher

    # Add handlers for commands and messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat_with_gpt))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    