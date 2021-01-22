test_code = open("testcode.mhl", "r")
# test_code = open("../DiscordBot with Python/discordbot.py", "r")

script_variables = {}

def print_function(to_print, is_raw_string):
	if is_raw_string == True:
		print(to_print[0])

def create_variable_function(name, value, var_dict):
	global script_variables
	new_var_to_create = {}
	if value.isdigit():
		new_var_to_create = {name:int(value)}
	else:
		value = value.replace('"', "")
		new_var_to_create = {name:value}
	script_variables = script_variables | new_var_to_create

def LogErrors(messages, line_number):
	print(f"Parse Error at line {line_number}")
	for message in messages:
		print(f"	{message}")

def parser():
	codeToParse = test_code.read()

	lines = codeToParse.split('\n')
	for word in lines:
		if word.startswith("//"):
			continue
		if word.startswith("print(") and word.endswith(")"):
			new_word = word.replace("print(", "")
			new_word = new_word.replace(")", "")
			if " + " in new_word:
				sum = 0
				to_add = new_word.split(" + ")
				for num in to_add:
					sum = sum + script_variables[num]
				print(sum)
			elif " - " in new_word:
				sum = 0
				to_add = new_word.split(" - ")
				for num in to_add:
					if to_add.index(num) == 0:
						sum = script_variables[num]
					else:
						sum = sum - script_variables[num]
				print(sum)
			elif " * " in new_word:
				sum = 0
				to_add = new_word.split(" * ")
				for num in to_add:
					if to_add.index(num) == 0:
						sum = script_variables[num]
					else:
						sum = sum * script_variables[num]
				print(sum)
			elif " / " in new_word:
				sum = 0
				to_add = new_word.split(" / ")
				for num in to_add:
					if to_add.index(num) == 0:
						sum = script_variables[num]
					else:
						sum = sum / script_variables[num]
				print(sum)
			elif new_word in script_variables:
				print(script_variables[new_word])
			else:
				LogErrors([f"There is no variable with the name '{new_word}'.", f"Try creating a variable with the name {new_word} and use that instead."], (lines.index(word)+1))
				return
		elif word.startswith("var "):
			new_word = word.replace("var ", "")
			if " = " in new_word:
				new_var = new_word.split(" = ")
				if list(new_var[0])[0].isdigit():
					LogErrors(["Variable names cannot start with a number."], (lines.index(word)+1))
					return
				elif "+" in new_var[0]:
					LogErrors(["Variable names cannot have a '+' sign in them."], (lines.index(word)+1))
					return
				elif "-" in new_var[0]:
					LogErrors(["Variable names cannot have a '-' sign in them."], (lines.index(word)+1))
					return
				elif "*" in new_var[0]:
					LogErrors(["Variable names cannot have a '*' sign in them."], (lines.index(word)+1))
					return
				elif "/" in new_var[0]:
					LogErrors(["Variable names cannot have a '/' sign in them."], (lines.index(word)+1))
					return
				else:
					create_variable_function(new_var[0], new_var[1], script_variables)
			else:
				print("You haven't used the '=' operator correctly.")
	# parser()

parser()
# print(script_variables)