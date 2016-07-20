import re
import latex2mathml
from bs4 import BeautifulSoup

def genImg(strques = ""):
	soup = BeautifulSoup(strques, "lxml")
	imglst = soup.findAll('img')

	if len(imglst) == 0:
		return [strques]

	for i in range(len(imglst)):
		strques = strques.replace(str(imglst[i]), "!img!")

	strqueslst = re.split("!img!", strques)

	lastLstQues = []
	resuLstQues = []
	indx = 0
	for istr in strqueslst[:-1]:
		lastLstQues.append(istr)
		lastLstQues.append(str(imglst[indx]['src']))
		indx += 1

	lastLstQues.append(strqueslst[-1])
	for ivalue in lastLstQues:
		if ivalue != "":
			resuLstQues.append(ivalue)

	print(strques)
	return resuLstQues



def getMathml(strques = ""):
	
	strques = strques.replace("\$", "!!")
	if strques.count("$") == 0 or strques.count("$") % 2 == 1:
		strques = strques.replace("!!", "$")
		return strques

	strsplit = re.split("\$", strques)
	laststr = []
	
	for i in range(len(strsplit)):
		if strsplit[i] == "":
			continue;

		if i%2 == 1: # math
			latex_input = strsplit[i]
			# print("=====", latex_input, len(latex_input))
			if latex_input != "":
				mathml_output = latex2mathml.convert(latex_input)
				# laststr += mathml_output.replace("<math>", '<math xmlns="http://www.w3.org/1998/Math/MathML">')
				laststr.append(mathml_output.replace("<math>", '<math xmlns="http://www.w3.org/1998/Math/MathML">'))
		else:
			laststr.append(strsplit[i])
			# laststr += strsplit[i]

	for i in range(len(laststr)):
		laststr[i] = laststr[i].replace("!!", "$")
	return laststr

if __name__ == '__main__':
	s = """这是计算题$3232+3232=$（    ）<img align="right" alt="Smiley face" height="100" src="images/login.png" width="100"/><img align="right" alt="Smiley face" height="100" src="images/trash.png" width="100"/>"""
	# s = 'ccc\$'
	print(genImg(s))
	# print(getMathml(s))

			 
