from comentarioDB import ComentarioDB
import text_analyzer
import json
candidate_labels = ["salary", "work-environment", "bosses","facilities"]


def process():
        db=ComentarioDB.getDataBase()    
        row_index=0
        comment_dataset=[]
        for comment in db.get_all_records():
              if "title" in comment.keys():
                     title=comment["title"]
              if "body" in comment.keys():                  
                      body=comment["body"]
                      print(body)
                      results_body=text_analyzer.analyze(body,candidate_labels)
                      print(results_body)
              if "Pros" in comment.keys():
                      pros=comment["Pros"]
              if "Cons" in comment.keys():
                      cons=comment["Cons"]
                      results_cons=text_analyzer.analyze(cons,candidate_labels)
                      print(results_cons)
              
                         
              #break
            


if __name__=='__main__':
         process()
 
 