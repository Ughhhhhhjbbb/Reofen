from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import zipfile
import shutil

# Replace with your actual token
TOKEN = '6528857056:AAG4nEuIfRreJmEoDMx-lVHVq0TErDx2lPA'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! Send me a zip file with your updated SDK source.')

def handle_document(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    file.download('updated_source.zip')
    
    # Unzip the uploaded file
    with zipfile.ZipFile('updated_source.zip', 'r') as zip_ref:
        zip_ref.extractall('updated_source')

    # Define paths
    sdk_folder_path = 'path/to/your/project/Sdk'  # Path to the SDK folder
    sdk_header_path = os.path.join(sdk_folder_path, 'sdk.hpp')  # Path to sdk.hpp

    # Delete old SDK folder and sdk.hpp
    if os.path.exists(sdk_header_path):
        os.remove(sdk_header_path)

    if os.path.exists(sdk_folder_path):
        shutil.rmtree(sdk_folder_path)  # Remove the SDK folder and all its contents

    # Define new SDK path from your bot's source
    new_sdk_path = 'SDK64/SDK'  # Path to the new SDK folder inside your bot structure

    # Copy new SDK folder to the user's project
    if os.path.exists(new_sdk_path):
        shutil.copytree(new_sdk_path, sdk_folder_path)

    update.message.reply_text('SDK source has been updated successfully!')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document.mime_type("application/zip"), handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
