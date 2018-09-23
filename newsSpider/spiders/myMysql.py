import pymysql.cursors

class myMysql:
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", db="mydemo", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def getLatestTime(self, tableName="web_news"):
        sqlstr = "select release_time from {0} order by release_time DESC".format(tableName)
        try:
            self.cursor.execute(sqlstr)
            result = self.cursor.fetchone()
            # print("result: {0}".format(result))

            if result:
                latest_release_time = str(result['release_time']).split(' ')[0]
            else:
                latest_release_time = "2018-01-01"
            print("latest_release_time：{0}".format(latest_release_time))

            return latest_release_time

        except Exception as e:
            raise e

        finally:
            self.cursor.close()

    def columnExist(self, tableName="web_news", columnName="link", columnValue=""):
        sqlstr = "select * from {0} where {1}='{2}'".format(tableName, columnName, columnValue)
        try:
            self.cursor.execute(sqlstr)
            result = self.cursor.fetchone()

            if result:
                return True
            else:
                return False
        except Exception as e:
            raise e
        finally:
            self.cursor.close()

# sql = myMysql()
# sql.getLatestTime()
# sql.getLatestTime("web_jwc_news")
# sql.getLatestTime("web_xsc_news")