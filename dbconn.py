import psycopg2

class DB:
    conn = 0
    cursor = 0
    def conn_with_db(self,name,user,pw,host):
        try:
            self.conn = psycopg2.connect(dbname=name, user=user, host=host, password=pw)
            self.cursor = self.conn.cursor()
            print("Connected success!")
        except Exception as e:
            print("I am unable to connect to the database {0}".format(e))