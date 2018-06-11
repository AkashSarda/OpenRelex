from postprocessing import PostProcessor
import spacy
import sys
a = PostProcessor()
filename = "news"

nlp = spacy.load("en_core_web_sm")

f = open(sys.argv[1])
for line in f.readlines():
	doc = nlp(line)
	for sent in doc.sents:
		print(sent.text)
		relations = a.information(sent.text)
		for rel in relations:
			text = ''
			for w in rel:
				text = text + ';' + w
			print(text)
			print("==========")
		print("+++++++++++")
#print(a.information("The revenue for the Premier League rights in Britain is supplemented by income from broadcast deals elsewhere, including in the United States, where NBC televises the matches, and in China, where the digital broadcaster PPTV holds the rights."))
