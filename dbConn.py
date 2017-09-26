import cx_Oracle
import phiredashboard

class orcl:
    username = '******'
    password = '*****'
    databaseName = "******"

    dsn = (username,password,databaseName)

    def __init__(self):
        self.db = cx_Oracle.connect (*self.dsn)
        self.cursor = self.db.cursor()

    def __enter__(self):
        return orcl()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    def printException (exception):
        error, = exception.args
        printf ("Error code = %s\n",error.code);
        printf ("Error message = %s\n",error.message);

    def dbExecuteFetchAll(self,sql):
        try:
            self.cursor.execute (sql)
            data = self.cursor.fetchall()
            return data
        except cx_Oracle.DatabaseError as exception:
            printf ('Failed to execute query on %s\n',databaseName)
            printException (exception)
            exit (1)

    def dbExecuteFetchOne(self,sql):
        try:
            self.cursor.execute (sql)
            data = self.cursor.fetchone()
            return data
        except cx_Oracle.DatabaseError as exception:
            printf ('Failed to execute query on %s\n',databaseName)
            printException (exception)
            exit (1)
