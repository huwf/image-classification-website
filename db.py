import mysql.connector


class MySQLUtil(object):
    host = 'localhost'
    user = 'darkskies'
    db = 'darkskies'

    # def __init__(self):
        # self.conn = self.get_connection()

    # def __del__(self):
    #     if self.cursor:
    #         self.cursor.close()
    #     self.conn.close()
    

    def _get_password(self):
        with open('config') as f:
            return f.read()


    def get_connection(self):
        return mysql.connector.connect(user=self.user,
                                      password=self._get_password(),
                                      host=self.host,
                                      database=self.db)



    def select_as_list(self, query, params=None):      
        conn = self.get_connection()  
        cursor = conn.cursor()
        cursor.execute(query, params)
        x = cursor.fetchall()
        return x

    def insert_value(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()


    def update_value(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()



