import os.path
import re
import sys

def expand_patterns():
	plength = 10
	wilds = re.compile("[X[]")
	global input_file
	if input_file is None:
		input_file = open("temp-user-pattern.txt", "w")
		input_file.write(user_pattern)
		input_file.close()
		input_file = "temp-user-pattern.txt"
	for summary in open(input_file, "r"):
		summary = summary.rstrip()
		m = wilds.search(summary)
		if m is None:
			print summary
			continue
		prefix = summary[:m.start()]
		summary = summary.replace("X", "\d")
		pattern = re.compile(summary)
		low = int("{}{}".format(prefix, "0" * (plength - len(prefix))))
		high = int("{}{}".format(prefix, "9" * (plength - len(prefix)))) + 1
		for did in range(low, high):
			if pattern.match(str(did)):
				print did
				
def summarize(patterns):
	model = patterns[0]
	x_count = list(model).count("X")
	prefix = model[:-(x_count + 1)]
	postfix = "X" * x_count
	numbers = []
	for pattern in patterns:
		numbers.append(pattern[:-x_count])
	if len(numbers) == 1: return model
	if len(numbers) == 10: return "{}X{}".format(prefix, postfix)
	if x_count > 0:
		summary = summarize_range(numbers)
	else:
		summary = summarize_range(patterns)
	return "{}{}".format(summary, postfix)
	
def summarize_range(patterns):
	prefix = patterns[0][:-1]
	numbers = []
	for pattern in patterns:
		numbers.append(pattern[-1])
	if len(numbers) == 10: return "{}X".format(prefix)
	for i in range(len(numbers)):
		number = int(numbers[i])
		if i == 0:
			summary = "{}".format(number)
			in_range = False
			first_in_range = True
			second_in_range = False
			prev = number
			continue
		if abs(number - prev) == 1:
			if not in_range:
				in_range = True
				second_in_range = True
				summary = "{}{}".format(summary, number)
			else:
				if second_in_range:
					second_in_range = False
					summary = "{}-{}".format(summary[:-1], number)
				else:
					summary = "{}{}".format(summary[:-1], number)
			prev = number
			continue
		summary = "{}{}".format(summary, number)
		in_range = False
		prev = number
	return "{}[{}]".format(prefix, summary)
	
def make_groups(patterns):
	model = patterns[0]
	x_count = list(model).count("X")
	prefix = model[:-(x_count + 1)]
	postfix = "X" * x_count
	numbers = []
	for pattern in patterns:
		numbers.append(pattern[:-x_count])
	if len(numbers) == 1: return [[model]]
	if x_count > 0:
		groups = make_groups_of_ten(numbers)
		for group in groups:
			for i in range(len(group)):
				group[i] = "{}{}".format(group[i], postfix)
		return groups
	else:
		return make_groups_of_ten(patterns)
		
def make_groups_of_ten(patterns):
	anchor = None
	container = []
	groups_of_ten = []
	for pattern in patterns:
		pattern = int(pattern)
		if anchor is None:
			anchor = (int(pattern) / 10) * 10
			container.append(str(pattern))
			continue
		if abs(anchor - pattern) < 10:
			container.append(str(pattern))
			continue
		groups_of_ten.append(container)
		anchor = (int(pattern) / 10) * 10
		container = [str(pattern)]
	groups_of_ten.append(container)
	return groups_of_ten

def summarize_patterns():
	hundreds = []
	output = []
	dids = []
	for did in open(input_file, "r"):
		dids.append(did.rstrip())
	gots = make_groups(dids)
	tens = []
	for got in gots:
		tens.append(summarize(got))
	t2h = []
	for i in range(len(tens)):
		ten = tens[i]
		if ten[-1] != "X" or i == len(tens) - 1:
			if len(t2h) > 0:
				gots = make_groups(t2h)
				t2h = []
				h = []
				for got in gots:
					h.append(summarize(got))
				hundreds += h + [ten]
			else:
				hundreds += [ten]
			continue
		t2h.append(ten)
	h2t = []
	for i in range(len(hundreds)):
		hundred = hundreds[i]
		if hundred[-2:] != "XX" or i == len(hundreds) - 1:
			if len(h2t) > 0:
				gots = make_groups(h2t)
				h2t = []
				t = []
				for got in gots:
					t.append(summarize(got))
				output += t + [hundred]
			else:
				output += [hundred]
			continue
		h2t.append(hundred)
	for pattern in output:
		print pattern
		
def usage():
	print "Usage: python patterns.py (summarize <file>|expand (<file>|<pattern>))"
	sys.exit(1)
	
if len(sys.argv) <> 3: usage()
command = sys.argv[1]
if command not in "summarize|expand": usage()
user_pattern = None
input_file = sys.argv[2]
if not os.path.exists(input_file):
	user_pattern = input_file
	input_file = None
if command == "summarize":
	if input_file is None:
		print "File not found"
		sys.exit(2)
	summarize_patterns()
elif command == "expand":
	expand_patterns()
sys.exit(0)