
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

     
def calculate_results(topiclist,opinions):
      results={}
      for topic, opinion in zip(topiclist,opinions):
            if not topic in results:
                      results[topic]=[opinion]
            else:
                      results[topic].append(opinion) 
      return results

def calculate_summarized(results):
       summarized={}
       for topic in results:       
         lista=results[topic]
         summarized[topic]=0
         neg_count = len(list(filter(lambda x: (x < 0), lista)))
         pos_count = len(list(filter(lambda x: (x >= 0), lista)))
         if neg_count>0:
              summarized[topic]+=1
         if pos_count>0:
              summarized[topic]+=1
       return summarized

#Devolvemos la cantidad de clusters
def calculate_k(topiclist, opinions):
      results=calculate_results(topiclist,opinions)
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
       plt.scatter(df['topic'], df['opinion'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
       plt.scatter(centroids[:, 0], centroids[:, 1],marker = "o", alpha = 0.9,s=100,c='red',label='Centroides')
       plt.title('Clúster de  topicos')
       plt.xlabel('Topicos')
       plt.ylabel('Opiniones')
       plt.legend()
       plt.show()


def main():
          Data= { 'topic':[1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3],
        'opinion':[-0.51,0.492,-0.60,0.90,1,0.88,0.65,0.75,0.90,-1,-0.7,-0.51,0.492,-0.60,0.90,1,0.88,0.65,0.75,0.90,-1,-0.7,-0.51,0.492,-0.60,0.90,1,0.88,0.65,0.75]
      
         }   
          make_cluster(Data)

if __name__=='__main__':
             main()

    

  
     