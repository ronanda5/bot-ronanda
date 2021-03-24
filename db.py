import pymysql.cursors


class DB:

    def __init__(self):
        super().__init__()
        self.connection = pymysql.connect(host='sql11.freesqldatabase.com',
                                          user='sql11397227',
                                          password='QbCgjusHvh',
                                          database='sql11397227',
                                          cursorclass=pymysql.cursors.DictCursor)

    def create_user(self, tag):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `users` (`tag`) VALUES (%s)"
                cursor.execute(sql, (tag,))
            self.connection.commit()

    def get_user(self, tag):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `users` WHERE `tag`=%s"
                cursor.execute(sql, (tag,))
                result = cursor.fetchone()
                return result

    def update_user(self, tag, server=None, stats=None):
        user = DB().get_user(tag)
        if server is not None:
            user['server'] = server
        if stats is not None:
            user['stats'] = stats
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "UPDATE `users` SET `server`=%s, `stats`=%s  WHERE `tag`=%s"
                cursor.execute(sql, (user['server'], user['stats'], tag))
            self.connection.commit()

    def create_character(self, name, user_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `characters` (`name`, `user_id`) VALUES (%s, %s)"
                cursor.execute(sql, (name, user_id))
            self.connection.commit()

    def update_character(self, name, signature=None, grade=None, assignation=None, matricule=None):
        character = DB().get_character(name=name)
        if signature is not None:
            character['signature'] = signature
        if grade is not None:
            character['grade'] = grade
        if assignation is not None:
            character['assignation'] = assignation
        if matricule is not None:
            character['matricule'] = matricule
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "UPDATE `characters` SET `signature`=%s, `grade`=%s, `assignation`=%s, `matricule`=%s WHERE `name`=%s"
                cursor.execute(sql, (character['signature'], character['grade'], character['assignation'], character['matricule'], name))
            self.connection.commit()

    def delete_character(self, name):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM `characters` WHERE `name`=%s"
                cursor.execute(sql, (name,))
            self.connection.commit()

    def get_character(self, id=None, name=None):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `characters` WHERE `id`=%s or `name`=%s"
                cursor.execute(sql, (id, name))
                result = cursor.fetchone()
                return result

    def get_characters(self, user_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `characters` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchall()
                return result
