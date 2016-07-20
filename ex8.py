import re
import latex2mathml

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
	s = "abcd$a^b$mmmm$a_b$"
	s = 'ccc\$'
	print(getMathml(s))

			 
