import telepot

bot = telepot.Bot(token="5320210497:AAFh8g9HJOxG4Om8KpqM5DZMO5f3WFQzMFQ")

# bot.sendMessage(chat_id="1921540131",
#                 text="[ALERT] Detected someone in the frame!")

bot.sendPhoto(chat_id="1921540131",
              photo=open("image.png", "rb"))