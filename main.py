import os
import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variable to store the header content
header_content = ''
file_name = ''

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me any file (image or otherwise), and I'll convert it into a C++ header file.")

# File handler to handle document uploads (images and other files)
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global header_content, file_name

    # Get the file information from the update
    document = update.message.document
    file = await context.bot.get_file(document.file_id)

    # Download the file
    file_path = await file.download_to_drive(f'./{document.file_name}')
    logger.info(f"File downloaded to: {file_path}")

    try:
        # Read the file contents as bytes (supports any file type)
        with open(file_path, 'rb') as f:
            byte_content = f.read()
            logger.info(f"Read {len(byte_content)} bytes from the file.")

        # Convert the file to a C++ header file
        file_name = document.file_name.replace('.', '_').upper() + "_H"
        header_content = f"#pragma once\n#include <cstdint>\n\n"
        header_content += f"/**\n * @author Reo_47\n * Telegram : Reohecks\n */\n\n"
        header_content += f"const std::uint8_t {file_name}[] = {{\n"

        byte_array = bytearray(byte_content)
        for i, byte in enumerate(byte_array):
            header_content += f"0x{byte:02x}, "
            if (i + 1) % 12 == 0:
                header_content += "\n"

        header_content = header_content.rstrip(', ') + "\n};\n"

        # Log the generated header content for debugging
        logger.info(f"Generated header content:\n{header_content}")

        # Save the header file temporarily
        header_file_path = f"./{file_name}.h"
        with open(header_file_path, 'w') as header_file:
            header_file.write(header_content)
        logger.info(f"Header file saved to: {header_file_path}")

        # Send back the converted header file
        await update.message.reply_document(document=InputFile(header_file_path))

    except Exception as e:
        logger.error(f"Error during file conversion: {e}")
        await update.message.reply_text("There was an error processing your file. Please try again.")

    finally:
        # Clean up the temporary files
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(header_file_path):
            os.remove(header_file_path)

# Error handler to log any errors
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Main function to set up the bot
def main():
    # Create an application instance using your bot token
    application = Application.builder().token("7535112403:AAFL_MsbRZVt43W22JhPuaVnJkrCcJ9eF1c").build()

    # Set up command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Log all errors
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
