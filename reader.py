from feeder import load_data

def read_from_web():
    return {"Nombre":"C","texto":"No me gusto"}

if __name__=='__main__':
         comentario= read_from_web()
         load_data(comentario)