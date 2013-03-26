from mysql import Db
class SsqbDb(Db):    
    def __init__(self, host=None, user=None, passwd=None):
        Db.__init__(self, host, user, passwd)
        self.queryNoVals("SET NAMES 'utf8'")
    def getDbs(self):
        sql = "SHOW DATABASES"
        if self.query(sql):
            return self.getAssoc()
    def getTables(self, db):
        sql = "SHOW TABLES FROM %s" % db
        if self.query(sql):
            return self.getRows()            
        
