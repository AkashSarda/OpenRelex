from algorithm_final import Extractor

class PostProcessor:
	def __init__(self):
		pass
	def getrelations(self, text):
		a = Extractor(text)
		return a.process()
	def removerepeatitions(self, relation):
		rel = []
		for ent in relation:
			if ent not in rel and ent not in ("'s"):
				rel.append(ent)
		return rel
	def information(self, text):
		relations = self.getrelations(text)
		cleaned = []
		for r in relations:
			if len(r) < 3:
				# rejected
				continue
			rel = self.removerepeatitions(r)
			cleaned.append(rel)
		return cleaned	
#a = PostProcessor()
#a.information("Facebook made a major bid last year to stream cricket matches from the Indian Premier League and is streaming Major League Baseball games, while Twitter has streamed baseball and professional hockey games.")
