
import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! قیمت خرید و فروش مثقال رو جداگانه وارد کن.")

state = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.replace(",", "")

    if user_id not in state:
        state[user_id] = {}

    if "buy" not in state[user_id]:
        state[user_id]["buy"] = int(text)
        await update.message.reply_text("قیمت فروش رو وارد کن:")
    else:
        state[user_id]["sell"] = int(text)
        buy = state[user_id]["buy"]
        sell = state[user_id]["sell"]
        del state[user_id]

        # محاسبه گرم
        buy_gram = int(buy / 4.3318)
        sell_gram = int(sell / 4.3318)

        message = f"""
💰 آبشده نقدی  ⬇️ 
◀️ هر مثقال :
🟢 فروش ما به شما :  {sell:,}
🔴 خرید ما از شما   :  {buy:,}

◀️ هر گرم :
🟢 فروش ما به شما :  {sell_gram:,}
🔴 خرید ما از شما   :  {buy_gram:,}

📞 جهت انجام معاملات تلفنی لطفا تماس بگیرید:
09133650701 - 03132239231
📢 @Mazane_Diamond
        """
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
        await update.message.reply_text("✅ ارسال به کانال انجام شد.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
