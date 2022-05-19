from comentarioDB import ComentarioDB
import text_analyzer
import json
candidate_labels = ["salary", "work-environment", "bosses"]


def process():
        db=ComentarioDB.getDataBase()    
        for comment in db.get_all_records():
              if "title" in comment.keys():
                     title=comment["title"]
              if "body" in comment.keys():
                      print("comenzando")
                      body=comment["body"]
                      #print(body)
                      #results=text_analyzer.analyze(body,candidate_labels)
                      #print(results)
              if "Pros" in comment.keys():
                      pros=comment["Pros"]
              if "Cons" in comment.keys():
                      cons=comment["Cons"]
                      results=text_analyzer.analyze(cons,candidate_labels)
                      print(results)
             
              #break
            


if __name__=='__main__':
         process()
 
 