from mysql import Db

class actions():
    
    db = None
    
    def init(self):
        pass
    
    def setDb(self, host=None, user=None, passwd=None):
        if host and user and passwd:
            self.db = Db(host, user, passwd)
    
    def listDbs(self):
        if self.db:
            return self.db.query('SHOW DATABASES')
