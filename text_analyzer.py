
from unittest import result
import topicanalizer
import sentimentanalyzer



def analyze(phrase, candidates):
      sentences=sentimentanalyzer.tokenize(phrase)
      results={}
      for sentence in sentences:
            feelings_results=sentimentanalyzer.analyze(sentence)
            topic_result=topicanalizer.analyze(sentence,candidates)      
            detected_topic=topic_result["labels"][0]
            detected_feeling=sentimentanalyzer.get_feeling(feelings_results)
            #print(sentence,detected_feeling,detected_topic)   
            results["topic"]=detected_topic
            results["feeling"] = detected_feeling
            results["phrase"]=sentence
      return results
if __name__=='__main__':
       #phrase = "The managers are wonderful. The chances are good"
       phrase="There's no chance of progress" # pos work-environment
       candidate_labels = ["salary", "work-environment", "bosses","progress"]
       analyze(phrase,candidate_labels)

