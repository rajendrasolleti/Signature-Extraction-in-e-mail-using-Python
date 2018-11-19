import importlib.util
import sys
import re
import pip

if importlib.util.find_spec('nltk') is None:
	pip.main(['install','nltk'])

import nltk
text = sys.argv[1]

def IdentifySignatureBlock(allsentences):
   IsSignatureStart = False
   sentenceposition=0;
   for sentence in allsentences:
      #print(sentence)
      IsSignatureStart = False
      sentence = sentence.lower()
      # 1. Check if the line contains any email address
      emails = re.findall(r'[\w\.-]+@[\w\.-]+', sentence)
      if len(emails)>0:
         IsSignatureStart=True	  
      # 2. Check if the line contains any phone numbers
      phonenumbers = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', sentence)
      if len(phonenumbers)>0:
         IsSignatureStart=True
      # 3. Check if the line contains any images
      lineswithimages = re.findall(r'(.ani|.bmp|.cal|.fax|.gif|.img|.jbg|.jpe|.jpeg|.jpg|.mac|.pbm|.pcd|.pcx|.pct|.pgm|.png|.ppm|.psd|.ras|.tga|.tiff|.wmf)',sentence)
      if len(lineswithimages)>0:
         IsSignatureStart=True
      # 4. Check if the line contains any hyperlinks
      links = re.findall(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})', sentence)
      if len(links)>0:
         IsSignatureStart=True
      # 5. Check if the line has more than 3 hyphens or underscores
      hyphenlines = re.findall(r'[_|-]{3,}',sentence)
      if len(hyphenlines)>0:
         IsSignatureStart=True
      # 6. Line has a sequence of 10 or more special characters
      specialcharacterlines = re.findall(r'([\*]|#|[\+]|[\^]|-|[\~]|[\&]|[///]|[\$]|_|[\!]|[\/]|[\%]|[\:]|[\=]){10,}',sentence)
      if len(specialcharacterlines)>0:
         IsSignatureStart=True
      # 7. The number of leading tabs is greater than or equal to 2
      lineswithmultipletabs = re.findall(r'[\t]{2,}',sentence)
      if len(lineswithmultipletabs)>0:
         IsSignatureStart=True
      # 8. If line above and below contain more than 80% of nouns
      if sentenceposition < len (sentences)-2 and sentenceposition>1:
         IsSignatureStart = checknouncount(allsentences[sentenceposition-1],sentence,sentences[sentenceposition+1])	  
      if IsSignatureStart:
         #print("Signature block identified at " + str(sentenceposition))
         return sentenceposition
         #print(allsentences[sentenceposition])
         break
      sentenceposition = sentenceposition + 1

def checknouncount(abovesentence, currentsentence, belowsentence):
   words = nltk.tokenize.word_tokenize(abovesentence)   
   postaggedwords = [pos[1] for pos in nltk.pos_tag(words)]
   countofnouns = postaggedwords.count('NN')+ postaggedwords.count('NNP')+postaggedwords.count('NNS')+ postaggedwords.count('NNPS')
   nounspercentabovesentence = float(countofnouns)/len(words)
   words = nltk.tokenize.word_tokenize(currentsentence)   
   postaggedwords = [pos[1] for pos in nltk.pos_tag(words)]
   countofnouns = postaggedwords.count('NN')+ postaggedwords.count('NNP')+postaggedwords.count('NNS')+ postaggedwords.count('NNPS')
   nounspercentcurrentsentence = float(countofnouns)/len(words)
   words = nltk.tokenize.word_tokenize(belowsentence)   
   postaggedwords = [pos[1] for pos in nltk.pos_tag(words)]
   countofnouns = postaggedwords.count('NN')+ postaggedwords.count('NNP')+postaggedwords.count('NNS')+ postaggedwords.count('NNPS')
   nounspercentbelowsentence = float(countofnouns)/len(words)
   if nounspercentabovesentence > 0.8 and nounspercentcurrentsentence>0.8 and nounspercentbelowsentence >0.8:
      return True
   else:
      return False   

try:
   nltk.tokenize.sent_tokenize(text)
except:
    nltk.download('punkt')
    from nltk import word_tokenize,sent_tokenize

sentences = nltk.tokenize.sent_tokenize(text)
sentencessplitonlinebreak = []
for sentence in sentences:
    sentencessplitonlinebreak.extend(list(filter(None, sentence.split('\r\n\r\n'))))
#print(sentencessplitonlinebreak)
signatureblockstartposition = IdentifySignatureBlock(sentencessplitonlinebreak)
if signatureblockstartposition is not None:
    del sentencessplitonlinebreak[signatureblockstartposition:]
print(sentencessplitonlinebreak)
