class Tag():
	"""doc"""
	def __init__(self, tag, **kwargs):
		self.tag = tag
		self.TopLevelTag = False
		self.is_single = False
		self.text = ""
		self.children = []
		self.attributes = {}
		#заполняем атрибуты
		if "is_single" in kwargs:
			self.is_single = kwargs.pop("is_single")
		if  kwargs:
			for key, value in kwargs.items():
				if key == "klass":
					self.attributes["class"] = " ".join(value)
				else:
					self.attributes[key.replace("_","-")] = value

	def addTag(self, other):
		if isinstance(other,TopLevelTag) or isinstance(other,Tag):
			self.children.append(other)

	def __str__(self):
		return self.makeText()

	def makeText(self, level=0):
		result = ""
		attrs = []
		for attribute, value in self.attributes.items():
			attrs.append('%s="%s"' % (attribute,value))

		attrs = " ".join(attrs)
		if attrs:
			attrs = " " + attrs

		if self.is_single:
			result += "\t"*level + "<{tag}{attrs}/>".format(tag=self.tag, attrs=attrs) + "\n"
		else:
			result += "\t"*level + "<{tag}{attrs}>".format(tag=self.tag, attrs=attrs, text=self.text) + "\n"
			if self.text:
				result += "\t"*(level + 1) + self.text + "\n"
			for child in self.children:
				result += child.makeText(level + 1) + "\n"
			result += "\t"*level + "</{tag}>".format(tag=self.tag)

		return result

class TopLevelTag():
	"""doc"""
	def __init__(self, tag):
		self.tag = tag
		self.children = []

	def __str__(self):
		return self.makeText()

	def makeText(self, level = 0):
		result = ""
		result += "\t"*level + "<{tag}>".format(tag=self.tag) + "\n"
		for child in self.children:
			result += child.makeText(level + 1) + "\n"
		result += "\t"*level + "</{tag}>".format(tag=self.tag)
		return result
	
	def addTag(self, other):
		if isinstance(other,TopLevelTag) or isinstance(other,Tag):
			self.children.append(other)

class Html():
	"""docstring for Html"""
	def __init__(self, **kwargs):
		self.children = []
		self.htmlfile = ""
		self.attributes = {}
		if  kwargs:
			for key, value in kwargs.items():
				if key == "klass":
					self.attributes["class"] = " ".join(value)
				else:
					self.attributes[key.replace("_","-")] = value

	def __str__(self):
		return self.makeText()
		
	def addTag(self, other):
		if isinstance(other,TopLevelTag) or isinstance(other,Tag):
			self.children.append(other)

	def makeText(self):
		result = ""
		result += "<html>\n"
		for child in self.children:
			result += child.makeText(level = 0) + "\n"
		result += "</html>"
		return result

	def makeFile(self, htmlfile):
		self.htmlfile = "htmlfile"
		result_text = "<!DOCTYPE html>\n" + self.makeText()
		if not result_text:
			print("There no text to print it out")
		else:
			f = open(htmlfile, "w", encoding="UTF-8")
			f.write(result_text)
			f.close()


#TEST
if __name__ == "__main__":
	OUTPUTFILE = "test.html"
	my_html = Html(lang="ru")

	head = TopLevelTag("HEAD")
	my_html.addTag(head)

	meta = Tag("meta", is_single = True, charset="UTF-8")
	head.addTag(meta)
	title = Tag("title")
	title.text="Document"
	head.addTag(title)

	body = TopLevelTag("BODY")
	my_html.addTag(body)
	
	div = Tag("div", klass=("container", "container-fluid"), id="lead")
	body.addTag(div)

	p = Tag("p")
	p.text = "another test"
	div.addTag(p)

	img = Tag("img", is_single=True, src="img1.jpg", data_image="responsive")
	div.addTag(img)

	div = Tag("div", klass=("container", "container-fluid"), id="lead2")
	body.addTag(div)

	p = Tag("p")
	p.text = """На протяжении последних десятилетий наблюдается неизменное ускорение темпов роста объема информации. 
	Кратко и емко данная ситуация была сформулирована в виде тезиса: «Информация — это единственный неубывающий ресурс общества". 
	Объем информации к 1800 г. удваивался каждые 50 лет, к 1950 г. – каждые 10 лет, к 1970 г. – каждые 5 лет, а к 1990 г. – ежегодно. 
	Следствием такого положения дел стал количественный барьер в процессах обработки информации. 
	Иногда информацию нет смысла собирать и хранить в связи с отсутствием возможности ее обработки и рационального использования. 
	Увеличение информации и растущий спрос на нее обусловили появление отрасли, связанной с автоматизацией обработки информации – информатикой.
	Основным направлением и предметом информатики является изучение и разработка информационных технологий на основе использования вычислительной техники. Информационная технология – это система приемов, способов и методов получения, передачи, обработки, хранения и представления информации. В настоящее время понятие «информационная технология» неразрывно связывают с использованием электронных средств передачи и обработки информации. В этом случае правильнее использовать термин «новая информационная технология», так как информационные технологии существовали и до появления компьютеров."""
	div.addTag(p)

	print(my_html)
	my_html.makeFile(OUTPUTFILE)
	
		
		
		