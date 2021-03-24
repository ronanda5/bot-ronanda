from bot import Bot
from config import Config

if __name__ == "__main__":
    bot = Bot()
    bot.run(Config.TOKEN)
