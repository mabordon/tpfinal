import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize
import nltk    
import nltk

def tokenize(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences


def analyze(sentence):

   _analyzer = SentimentIntensityAnalyzer()
   scores = _analyzer.polarity_scores(sentence)
   return scores

def get_feeling(scores):
     max=0
     feeling=None
     for category in scores.keys():
         if category in ('pos','neg'):
            if max<scores[category]:
                 max=scores[category]
                 feeling=category
     return feeling     


if __name__=='__main__':
      sentences=tokenize("The environment is so stressful. The salary is good")
  
      for sentence in sentences:
            print(analyze(sentence))

