from comentarioDB import ComentarioDB
from sentimentanalyzer import negative_or_positive
import text_analyzer
import json
candidate_labels = ["salary", "work-environment", "bosses","facilities"]

def process():
        db=ComentarioDB.getDataBase()      
        corpus=None 
        topiclist=[]
        opinionlist=[]
        rowindex=0
        for comment in db.get_all_records():
              if "title" in comment.keys():
                     title=comment["title"]
              if "body" in comment.keys():                  
                      corpus=comment["body"]               
              if "Pros" in comment.keys():
                      corpus=comment["Pros"]               
              if "Cons" in comment.keys():
                      corpus=comment["Cons"]
              if corpus:
                       results_cons=text_analyzer.analyze(corpus,candidate_labels)
                       print(results_cons)
                       indice=candidate_labels.index(results_cons['topic'])
                       topiclist.append(indice)
                       opinionlist.append(results_cons['feeling'])
                       if rowindex==10: break
                       rowindex+=1
        dict_object={"topic":topiclist,"opinion":opinionlist}      
        json_string=json.dumps(dict_object)             
        print(json_string)   
        jsonFile = open("./clusterprocessor/input/bajada1.json", "w")  
        jsonFile.write(json_string)
        jsonFile.close()        
                         


if __name__=='__main__':
         process()
 
 