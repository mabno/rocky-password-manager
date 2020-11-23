def readFile(file, binary=False):
	mode = 'r' if not binary else 'rb'
	with open(file, mode) as reader:
		return(reader.read())

def writeFile(file, content, binary=False):
	mode = 'w' if not binary else 'wb'
	with open(file, mode) as writer:
		writer.write(content)