import re
import latex2mathml

s = "abcd$a^b$mmmm$a_b$"
result = re.findall('\$.*\$', s)
strsplit = re.split("\$", s)
print(s, strsplit)

laststr = ""
if len(strsplit) % 2 == 0:
	print("please input double '$'!")
else:
	for i in range(len(strsplit)):
		if i%2 == 1: # math
			latex_input = strsplit[i]
			print("=====", latex_input)
			mathml_output = latex2mathml.convert(latex_input)
			laststr += mathml_output.replace("<math>", '<math xmlns="http://www.w3.org/1998/Math/MathML">')
		else:
			laststr += strsplit[i]

print(laststr)

			 
