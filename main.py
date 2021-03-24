from bot import Bot
from config import Config
from db import DB


if __name__ == "__main__":

    # load env variables
    config = Config()

    # test database connection runs without problems
    db = DB(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_DATABASE)

    # bot goes brrr
    Bot(config.COMMAND_PREFIX, db).run(config.TOKEN)
