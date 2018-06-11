import spacy
nlp = spacy.load("en_core_web_sm")

class Node:
	def __init__(self, token):
		self.token = token
		self.children = token.children
		self.text = token.text
		self.head = token.head

	def append_text(self, text):
		self.text = text + ' ' + self.text

class Extractor:
	def __init__(self, text):
		self.doc = nlp(text)
		self.ents = self.doc.ents
		self.nounchunks_roots = {}

	def givenounchunks(self, node):
		text = ''
		# for child in node.token.children:
		# 	if child.dep_ in ('compound', 'poss'):
		# 		nd = self.givenounchunks(Node(child))
		# print(node.text, " :::::::::::: ", self.nounchunks_roots)
		if node.text in self.nounchunks_roots.keys():
			node.text = self.nounchunks_roots[node.text]
		return node

	def resolvemodifiers(self, nd):
		modifiers = ['compound', 'advmod', 'amod', 'neg', 'npadvmod', 'num', 'number', 'quantomod', 'vmod', 'poss', 'nummod']
		#for child in nd.children:
		#	if child.dep_ in modifiers:
		#		n = self.resolvemodifiers(Node(child))
		#		nd.append_text(n.text)
		i = nd.token.i
		while True:
			token = self.doc[i - 1]
			if token in nd.token.children:
				if token.dep_ in modifiers:
					n = self.resolvemodifiers(Node(token))
					nd.text = n.text + ' ' + nd.text
				i -= 1
			else:
				break
		return nd

	def giveverbrelations(self, verb):
		rels = []
		modifiers = ['compound', 'advmod', 'amod', 'neg', 'npadvmod', 'num', 'number', 'quantomod', 'vmod', 'poss', 'nummod']
		for child in verb.token.children:
			if child.dep_ in modifiers:
				continue
			if child.dep_ in ('dobj', 'prep', 'ccomp', 'xcomp', 'advcl', 'pcomp', 'relcl','pobj', 'attr', 'acomp', 'acl'):
				rel = self.giverelations(Node(child))
				rel.insert(0, verb.text)
				rels.append(rel)
			if child.dep_ == 'conj':
				child = self.resolvemodifiers(Node(child))
				rel = self.giveverbrelations(child)
				rels.extend(rel)
		return rels

	def giverelations(self, node):
		rels = []
		modifiers = ['compound', 'advmod', 'amod', 'neg', 'npadvmod', 'num', 'number', 'quantomod', 'vmod', 'poss', 'nummod']
		node = self.resolvemodifiers(node)
		flag = 0
		for child in node.token.children:
			if child.dep_ in modifiers:
				continue
			if child.dep_ in ('prep', 'xcomp', 'pcomp', 'relcl', 'pobj', 'dobj', 'advcl', 'ccomp', 'appos', 'conj', 'acomp', 'acl') and flag == 0:
				rel = self.giverelations(Node(child))
				rel.insert(0, node.text)
				rels.extend(rel)
		if rels == []:
			return [node.text]
		else:
			pass
		return rels

	def process(self):
		subjs = []
		relations = []
		for token in self.doc:
			if token.dep_ == 'nsubj' or token.dep_ == 'nsubjpass' or token.dep_ == 'attr':
				subjs.append(self.resolvemodifiers(Node(token)))
		for node in subjs:
			headword = self.resolvemodifiers(Node(node.head))
			rels = self.giveverbrelations(headword)
			for child in node.token.children:
				if child.dep_ in ('prep', 'relcl', 'xcomp', 'pcomp', 'appos'):
					rel = self.giverelations(Node(child))
					rels.append(rel)
				if child.dep_ == 'conj':
					child = self.resolvemodifiers(Node(child))
					rel = self.giverelations(child)
					rels.append(rel)
			for r in rels:
				if type(r) != type("string"):
					r.insert(0, node.text)
			relations.extend(rels)
		return relations

#a = Extractor("As a child, Dennis moved with his family to Summit, New Jersey, where he graduated from Summit High School.")
#a = Extractor("Gaurav, being from Nagpur, knows how to speak in Marathi.")
# a = Extractor("Allison attracted intense interest from across Europe following his displays for Roma in Champions League.")
#a = Extractor("Real Madrid sign Brazilian star Rodrigo Rodrigues.")
#a = Extractor("After enrolling in a computer science PhD program at Stanford University, Page was in search of a dissertation theme and considered exploring the mathematical properties of the World Wide Web, understanding its link structure as a huge graph.")
#a = Extractor("Adam Levine has been directed to appear before the police for a joint investigation on Saturday.")
#a = Extractor("Born in Honolulu, Hawaii, Obama is a US Citizen.")
#a = Extractor("Dennis of New Jersey is a computer scientist.")
#a = Extractor("The winner will ascend to one of the few roles in American politics with the prestige to act as a counterweight to the presidency and instantly be a player in the 2020 presidential race.")
#a = Extractor("The main goal of relation extraction is to determine a type of relation between two target entities that appear together in a text.")
#a = Extractor("Wikidata acts as central storage for the structured data of its Wikimedia sister projects including Wikipedia, Wikivoyage, Wikisource, and others.")
#a = Extractor("Trump disinvites Philadelphia Eagles from White House visit, citing anthem dispute.")
#a = Extractor("Despite Trump’s public bravado, his legal team readies for a showdown with Mueller.")
#a = Extractor("Prosecutors with special counsel Robert S. Mueller III say the former Trump campaign chairman and an associate repeatedly contacted two members of a public relations firm and asked them to falsely testify about secret lobbying they did at Manafort’s behest.")
#a = Extractor("According to Gizmodo, company managers notified employees during a meeting Friday.")
#a = Extractor("Facing both public pressure and unrest from within its own company, Google will not renew its contract to help build artificial intelligence tools for the military, according to a report by Gizmodo's Kate Conger.")
#a = Extractor("Diane Greene, CEO of Google Cloud, informed employees of the company's decision on Friday, unnamed sources told Gizmodo.")
#a = Extractor("When the extent of Google's participation in Project Maven became public, it ignited a civil war inside Google.")
#a = Extractor("It could also encourage more people to take part in the trading of these currencies.")
#a = Extractor("As of now, the system can identify 48 different animal species in an image and can also give the count of each species present.")
#a = Extractor("Born in Michigan in 1973, Larry Page's parents were both computer experts, so it was no surprise that he studied computer engineering at Stanford University.")
#a = Extractor("As a research project at Stanford University, Page and Brin created a search engine that listed results according to the popularity of the pages, after concluding that the most popular result would often be the most useful.")
#a = Extractor("In 2006, Google purchased the most popular website for user-submitted streaming videos, YouTube, for $1.65 billion in stock.")
#a = Extractor("Page focused on the problem of finding out which web pages link to a given page, considering the number and nature of such backlinks as valuable information for that page.")
#a = Extractor("Brin was born in Moscow in the Soviet Union, to Russian Jewish parents, Yevgenia and Mikhail Brin, both graduates of Moscow State University.")
#a = Extractor("There have been disagreements within the G-7 in the past, including a long chill between the Europeans and President George W. Bush over the Iraq war.")
#a = Extractor("And Mark Dubowitz, the chief executive of the Foundation for Defense of Democracies, said that because of “real indignation and real frustration” on the part of European leaders who are extremely angry at Mr. Trump, the “venting process is likely to continue” throughout the meeting.")
#a = Extractor("The ill will among America’s allies is a striking contrast to the praise Mr. Trump has heaped on North Korea, one of the country’s most enduring adversaries, before his historic meeting next week with Kim Jong-un, the country’s normally reclusive leader.")
#a = Extractor("Facebook made a major bid last year to stream cricket matches from the Indian Premier League and is streaming Major League Baseball games, while Twitter has streamed baseball and professional hockey games.")
#print(a.process())
#relations = a.process()

#for r in relations:
#	print(r)
#for ent in a.ents:
#	print(ent.text, ent.label_)
