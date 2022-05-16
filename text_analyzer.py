
import topicanalizer
import sentimentanalyzer



def analyze(phrase, candidates):
      sentences=sentimentanalyzer.tokenize(phrase)
      for sentence in sentences:
            feelings_results=sentimentanalyzer.analyze(sentence)
            topic_result=topicanalizer.analyze(sentence,candidates)      
            detected_topic=topic_result["labels"][0]
            detected_feeling=sentimentanalyzer.get_feeling(feelings_results)
            print(detected_feeling,detected_topic)   
            
if __name__=='__main__':
       phrase = "The managers are sick"
       candidate_labels = ["salary", "work-environment", "bosses"]
       analyze(phrase,candidate_labels)

