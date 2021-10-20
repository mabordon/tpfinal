from itbatools import get_itba_logger
from comentarioDB import ComentarioDB

logger=get_itba_logger("feeder",screen=True)

comentarios=ComentarioDB.getDataBase()

def load_data(comentario):  
  try:
     
      comentarios.insert_comentario(comentario)
      logger.info(f"Ejecutando la inserción del comentario")       
  except Exception as e: 
                      logger.error(e)

def read_from_web():
    return {"Nombre":"C","texto":"No me gusto"}

if __name__=='__main__':
         comentario= read_from_web()
         load_data(comentario)   