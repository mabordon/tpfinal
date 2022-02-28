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

if __name__=='__main__':
      sentences=tokenize("I am sure that is the reason why education is so important. What a beautiful day")
      for sentence in sentences:
            print(analyze(sentence))

