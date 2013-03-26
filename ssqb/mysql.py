import MySQLdb

class Db:
    def __init__(self, host=None, user=None, passwd=None):
        try:
            self.connection = MySQLdb.connect(host, user, passwd)
            self.cursor = self.connection.cursor()
        except MySQLdb.OperationalError, message:
            print "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
            return False
    def queryNoVals(self,query):
        if(hasattr(self,'cursor')):
            self.cursor.execute(query)
            return True
        else:
            return False
    def query(self, query):
        if(hasattr(self,'cursor')):
            self.cursor.execute(query)
            self.data = self.cursor.fetchall()
            self.fields = self.cursor.description
            self.fieldlist = [];
            for name in self.fields:
                self.fieldlist.append(name[0])
            self.data
            return True
        else:
            return False
    def getAssoc(self):
        assoc = []
        for row, data in enumerate(self.getRows()):
            rowdata = {}
            for i, item in enumerate(data):
                rowdata[self.fieldlist[i]]  = item
            assoc.append(rowdata)
        return assoc
    def getRows(self):
        return self.data
    def getFields(self):
        return self.fieldlist
    def lastInsertId(self):
        return self.cursor.lastrowid
    def Close(self):
            self.cursor.close()
            self.connection.close()
    def __del__(self):
        self.Close()
