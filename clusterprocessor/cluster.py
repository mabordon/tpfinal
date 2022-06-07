
import matplotlib
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import json
 

input='./clusterprocessor/input/bajada.json'
output='./clusterprocessor/output/cluster.png'
     


def groupbytopicsandopinion(topiclist,opinions):
      results={}
      for topic, opinion in zip(topiclist,opinions):
            if not topic in results:
                      results[topic]=[opinion]
            else:
                      results[topic].append(opinion) 
      print("Imprimiendo resultados")
      print(results)
      return results

def calculate_summarized(results):
       summarized={}
       for topic in results:       
         lista=results[topic]
         print("Imprimiendo la lista")
         print(topic,lista)
         summarized[topic]=0
         neg_count = len(list(filter(lambda x: (x < 0), lista)))
         pos_count = len(list(filter(lambda x: (x >= 0), lista)))
         if neg_count>0:
              summarized[topic]+=1
         if pos_count>0:
              summarized[topic]+=1
         print("Estadisticas=>",topic,summarized[topic])
       return summarized

#Devolvemos la cantidad de clusters
def calculate_k(topiclist, opinions):
      results=groupbytopicsandopinion(topiclist,opinions)
      summarized=calculate_summarized(results)      
      k=0
      for topic in summarized:
           k+=summarized[topic]
      print(k)
      return k
                     


def make_cluster(Data): 
       df = DataFrame(Data,columns=['topic','opinion'])
       kmeans = KMeans(n_clusters=calculate_k(Data['topic'],Data['opinion'])).fit(df)
       centroids = kmeans.cluster_centers_
       print(centroids)
       print(kmeans.labels_)     
       colores=['red','green','blue','cyan','yellow','violet','orange','black']
       asignar=[]
       for row in kmeans.labels_:
            asignar.append(colores[row])


       plt.scatter(df['topic'], df['opinion'], marker="o",s=100, alpha=0.5,c=asignar) 
       plt.scatter(centroids[:, 0], centroids[:, 1],marker = "*", alpha = 0.9,s=300,c='red',label='Centroides')
       plt.title('Clúster de  tópicos')
       plt.xlabel('Tópicos')
       plt.ylabel('Opiniones')
       plt.legend()
       #plt.show()
       plt.savefig(output)


def process():    
          data = open(input,)
          data = json.load(data)             
          make_cluster(data)
          print("Done")
        

if __name__=='__main__':  
                 process()

    

  
     