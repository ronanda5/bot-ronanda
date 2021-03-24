import pymysql.cursors


class DB:

    def __init__(self, host, user, password, database):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()
    
    def connect(self):
        return pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               database=self.database,
                               cursorclass=pymysql.cursors.DictCursor)

    def create_user(self, tag):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `users` (`tag`) VALUES (%s)"
                cursor.execute(sql, (tag,))
            connection.commit()

    def get_user(self, tag):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `users` WHERE `tag`=%s"
                cursor.execute(sql, (tag,))
                result = cursor.fetchone()
                return result

    def update_user(self, tag, server=None, stats=None):
        user = self.get_user(tag)
        if server is not None:
            user['server'] = server
        if stats is not None:
            user['stats'] = stats
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `users` SET `server`=%s, `stats`=%s  WHERE `tag`=%s"
                cursor.execute(sql, (user['server'], user['stats'], tag))
            connection.commit()

    def create_character(self, name, user_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `characters` (`name`, `user_id`) VALUES (%s, %s)"
                cursor.execute(sql, (name, user_id))
            connection.commit()

    def update_character(self, name, signature=None, grade=None, assignation=None, matricule=None):
        character = self.get_character(name=name)
        if signature is not None:
            character['signature'] = signature
        if grade is not None:
            character['grade'] = grade
        if assignation is not None:
            character['assignation'] = assignation
        if matricule is not None:
            character['matricule'] = matricule
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `characters` SET `signature`=%s, `grade`=%s, `assignation`=%s, `matricule`=%s WHERE `name`=%s"
                cursor.execute(sql, (character['signature'], character['grade'], character['assignation'], character['matricule'], name))
            connection.commit()

    def delete_character(self, name):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `characters` WHERE `name`=%s"
                cursor.execute(sql, (name,))
            connection.commit()

    def get_character(self, id=None, name=None):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `characters` WHERE `id`=%s or `name`=%s"
                cursor.execute(sql, (id, name))
                result = cursor.fetchone()
                return result

    def get_characters(self, user_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `characters` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchall()
                return result
