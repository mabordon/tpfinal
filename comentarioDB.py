from pymongo import MongoClient
from itbatools import get_db_property_hook
from singleton import Singleton


class ComentarioDB(metaclass=Singleton): 
    def __init__(self,_dbconfigurator):      
           self._mongoClient = MongoClient(_dbconfigurator.host,
                                           _dbconfigurator.port)
           self._db=self._mongoClient.comentario
           self._comentarios=self._db.comentarios
    def insert_comentario(self,comentario):
        self._comentarios.insert_one(comentario)
    def delete_comentario(self,comentario):
        self._comentarios.delete_one(comentario)  
    def printrecords(self):
             for comentario in self._comentarios.find({}):
                 print(comentario)
    def test_add(self):
           comentario={"body":"Hello"}
           self.insert_comentario(comentario)
    def test_delete(self): 
           comentario={"body":"Hello"} 
           self.delete_comentario(comentario)
    @classmethod
    def getDataBase(cls):
       _dbconfigurator=get_db_property_hook()
       return ComentarioDB(_dbconfigurator) 

    

if __name__=='__main__':
        db=ComentarioDB.getDataBase()    
        db.test_delete()  
        db.test_add()
        db.printrecords()
        