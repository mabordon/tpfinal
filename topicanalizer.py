from transformers import pipeline

classifier = pipeline("zero-shot-classification")

def analyze(sequence,candidate_labels):
   result=classifier(sequence, candidate_labels)
   return result

if __name__=='__main__':
   sequence = "pay is way under market"
   candidate_labels = ["salary", "work-environment", "bosses"]
   result=analyze(sequence,candidate_labels)
   print(result)
