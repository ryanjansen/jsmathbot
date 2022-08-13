from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters

SIDES, TRIANGLE, PARALLEL = range(3)

async def hello(update, context):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def sides(update, context):
     reply_keyboard = [["3", "4", "Others"]]
     await update.message.reply_text(
        "How many sides does the shape have?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="How many sides?"
        ))

     return SIDES

async def triangle(update, context):
     reply_keyboard = [["2", "3", "Others"]]
     await update.message.reply_text(
        "How many equal sides does the triangle have?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="How many equal sides?"
        ))

     return TRIANGLE


async def whichTriangle(update, context):
    equal_sides = update.message.text

    if (equal_sides == "Others"):
        await update.message.reply_text(
            "Your shape is a Scalene Triangle", reply_markup=ReplyKeyboardRemove()
        )
    elif (equal_sides == "2"):
        await update.message.reply_text(
            "Your shape is a Isoceles Triangle", reply_markup=ReplyKeyboardRemove()
        )
    elif (equal_sides == "3"):
        await update.message.reply_text(
            "Your shape is a Equilateral Triangle", reply_markup=ReplyKeyboardRemove()
        )

    return ConversationHandler.END

async def dontcare(update, context):
    await update.message.reply_text(
        "Your shape sucks", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text(
        "Ok, we'll stop finding your shape", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

bot = ApplicationBuilder().token('5412622826:AAFi0DbXDB3qTEICF7OvdDzXbOZJIxsWnX0').build()

bot.add_handler(CommandHandler("hello", hello))

shape_handler = ConversationHandler(
        entry_points=[CommandHandler("shape", sides)],
        states={
            SIDES: [MessageHandler(filters.TEXT & filters.Regex("^Others$"), dontcare),
                    MessageHandler(filters.TEXT & filters.Regex("^3$"), triangle)],
            TRIANGLE: [MessageHandler(filters.TEXT & filters.Regex("^(2|3|Others)$"), whichTriangle)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

bot.add_handler(shape_handler)

bot.run_polling()
