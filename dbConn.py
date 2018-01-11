import cx_Oracle
import phiredashboard

class orcl:
    username = 'SYSADM'
    password = '******'
    databaseName = "PSPHIRE1"

    dsn = (username,password,databaseName)

    def __init__(self):
        self.db = cx_Oracle.connect (*self.dsn)
        self.cursor = self.db.cursor()

    def __enter__(self):
        return orcl()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    def printException (self, exception):
        error = exception.args
        print ("Error code = %s\n",error.code);
        print ("Error message = %s\n",error.message);

    def dbExecuteFetchAll(self, sql, params=None):
        try:
            if params is not None:
              self.cursor.execute (sql, params)
              data = self.cursor.fetchall()
              return data
            else:
              self.cursor.execute (sql)
              data = self.cursor.fetchall()
              return data
        except cx_Oracle.DatabaseError as exception:
            print ('Failed to execute query on database: ', self.databaseName)
            self.printException (exception)
            exit (1)

    def dbExecuteFetchOne(self, sql, params=None):
        try:
            if params is not None:
              self.cursor.execute (sql, params)
              data = self.cursor.fetchone()
              return data
            else:
              self.cursor.execute (sql)
              data = self.cursor.fetchone()
              return data
		
        except cx_Oracle.DatabaseError as exception:
            print ('Failed to execute query on database: ',self.databaseName)
            self.printException (exception)
            exit (1)
