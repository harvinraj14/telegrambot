from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler

# Define states
FIRST, SECOND, THIRD = range(3)


async def start(update: Update, context: CallbackContext) -> int:
    """Initial welcome message and menu"""
    print("Got start command!")  # Debug print

    # Clear any existing conversation data
    context.user_data.clear()

    welcome_text = (
        "👋 Welcome to 6 AIS!\n"
        "How can we assist you today?"
    )

    keyboard = [
        [InlineKeyboardButton("Enquiry on specific person", callback_data='general')],
        [InlineKeyboardButton("Technical Expertise", callback_data='technical')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    return FIRST


async def first_choice(update: Update, context: CallbackContext) -> int:
    """Handle first level menu choices"""
    query = update.callback_query
    await query.answer()

    if query.data == 'general':
        keyboard = [
            [InlineKeyboardButton("Asset Team Lead", callback_data='asset_lead')],
            [InlineKeyboardButton("Senior Product Engineer", callback_data='senior_eng')],
            [InlineKeyboardButton("Product Engineer", callback_data='prod_eng')],
            [InlineKeyboardButton("Data Analyst", callback_data='data_analyst')]
        ]
        await query.edit_message_text(
            text="📋 Who would you like to contact?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SECOND

    elif query.data == 'technical':
        keyboard = [
            [InlineKeyboardButton("Hardware", callback_data='hardware')],
            [InlineKeyboardButton("Software", callback_data='software')]
        ]
        await query.edit_message_text(
            text="🔧 What type of technical assistance do you need?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SECOND


async def second_choice(update: Update, context: CallbackContext) -> int:
    """Handle second level choices"""
    query = update.callback_query
    await query.answer()

    # For General Enquiry contacts
    contacts = {
        'asset_lead': """
👤 Asset Team Lead
Name: [Name]
Role: Asset Management Lead
Email: [Email]
Phone: [Phone]
Location: [Location]
""",
        'senior_eng': """
👤 Senior Product Engineer
Name: [Name]
Role: Senior Product Engineer
Email: [Email]
Phone: [Phone]
Location: [Location]
""",
        'prod_eng': """
👤 Product Engineer
Name: [Name]
Role: Product Engineer
Email: [Email]
Phone: [Phone]
Location: [Location]
""",
        'data_analyst': """
👤 Data Analyst
Name: [Name]
Role: Data Analytics
Email: [Email]
Phone: [Phone]
Location: [Location]
"""
    }

    if query.data in contacts:
        keyboard = [
            [InlineKeyboardButton("« Back to Main Menu", callback_data='restart')],
            [InlineKeyboardButton("New Search", callback_data='new_search')]
        ]
        await query.edit_message_text(
            text=f"{contacts[query.data]}\n\nNeed anything else?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return THIRD

    elif query.data == 'hardware':
        keyboard = [
            [InlineKeyboardButton("3D Printing", callback_data='3d_printing')],
            [InlineKeyboardButton("Hardware Testing", callback_data='hw_testing')],
            [InlineKeyboardButton("Equipment Support", callback_data='equipment')],
            [InlineKeyboardButton("« Back to Main Menu", callback_data='restart')]
        ]
        await query.edit_message_text(
            text="🔨 Select the hardware assistance you need:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SECOND

    elif query.data == 'software':
        keyboard = [
            [InlineKeyboardButton("App Development", callback_data='app_dev')],
            [InlineKeyboardButton("System Integration", callback_data='sys_integration')],
            [InlineKeyboardButton("Data Analytics", callback_data='data_analytics')],
            [InlineKeyboardButton("« Back to Main Menu", callback_data='restart')]
        ]
        await query.edit_message_text(
            text="💻 Select the software assistance you need:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SECOND

    # Technical Support responses with detailed contact information
    tech_responses = {
        '3d_printing': """
🖨️ 3D Printing Support
Contact Person: 
Role: 
Email: 
Phone: 


Available hours: 9AM - 5PM (Mon-Fri)

""",
        'hw_testing': """
🔧 Hardware Testing Support
Contact Person: 
Role: 
Email: 
Phone: 


Available hours: 8AM - 5PM (Mon-Fri)

""",
        'equipment': """
⚙️ Equipment Support
Contact Person: 
Role: 
Email: 
Phone:


Available hours: 8AM - 5PM (Mon-Fri)

""",
        'app_dev': """
📱 App Development Support
Contact Person: 
Role: 
Email: 
Phone:


Available hours: 8AM - 5PM (Mon-Fri)

""",
        'sys_integration': """
🔄 System Integration Support
Contact Person: 
Role: 
Email: 
Phone: 


Available hours: 8AM - 5PM (Mon-Fri)

""",
        'data_analytics': """
📊 Data Analytics Support
Contact Person: 
Role: 
Email: 
Phone: 
Location:

Available hours: 8AM - 5PM (Mon-Fri)

"""
    }

    if query.data in tech_responses:
        keyboard = [
            [InlineKeyboardButton("« Back to Main Menu", callback_data='restart')],
            [InlineKeyboardButton("New Search", callback_data='new_search')]
        ]
        await query.edit_message_text(
            text=f"{tech_responses[query.data]}\n\nNeed anything else?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return THIRD


async def third_choice(update: Update, context: CallbackContext) -> int:
    """Handle return to main menu or new search"""
    query = update.callback_query
    await query.answer()

    if query.data == 'restart':
        keyboard = [
            [InlineKeyboardButton("Enquiry on specific person", callback_data='general')],
            [InlineKeyboardButton("Technical Expertise", callback_data='technical')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="👋 Welcome to 6 AIS!\nHow can we assist you today?",
            reply_markup=reply_markup
        )
        return FIRST

    elif query.data == 'new_search':
        context.user_data.clear()
        await query.message.reply_text(
            text="👋 Welcome to 6 AIS!\nHow can we assist you today?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Enquiry on specific person", callback_data='general')],
                [InlineKeyboardButton("Technical Expertise", callback_data='technical')]
            ])
        )
        return FIRST

    return ConversationHandler.END


def main():
    TOKEN = "8031336760:AAGEh-SLOraIdj1YvCH6dlVv_dRCaTKtmXA"

    print("Starting AssetSIX Bot...")
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(first_choice)],
            SECOND: [CallbackQueryHandler(second_choice)],
            THIRD: [CallbackQueryHandler(third_choice)]
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    print("Bot is ready!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()