"""
simple program to generate and store the 256 rules
that define elementary cellular automata.
"""
rules = []

for i in range(0, 256):
	rule = format(i, "#010b")[2:]
	rules.append(rule)

rules = "\n".join(rules)

f = open("rules.txt", "w+")
f.write(rules)
f.close()