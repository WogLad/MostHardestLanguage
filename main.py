test_code = open("testcode.mhl", "r")
# test_code = open("../DiscordBot with Python/discordbot.py", "r")

class MhlLibrary(object):
	"""docstring for MhlLibrary"""
	library_name = ""
	functions = []
	def __init__(self, name, functions):
		self.library_name = name
		self.functions = functions

script_variables = {}

def print_function(to_print, line_number):
	if to_print in script_variables:
		print(script_variables[to_print])
	else:
		LogErrors([f"There is no variable with the name {to_print}"], line_number)

def print_function_string(to_print, line_number):
	if to_print.startswith('"') and to_print.endswith('"'):
		to_print = to_print.replace('"', '')
		print(to_print)
	else:
		LogErrors(["Put the string you want to print in doble quotes."], line_number)

def add(nums_to_add):
	sum = 0
	for num in nums_to_add:
		sum = sum + num
	return sum

def subtract(nums_to_add):
	difference = 0
	for num in nums_to_add:
		if nums_to_add.index(num) == 0:
			difference = num
		else:
			difference = difference - num
	return difference

def multiply(nums_to_add):
	product = 0
	for num in nums_to_add:
		if nums_to_add.index(num) == 0:
			product = num
		else:
			product = product * num
	return product

def divide(nums_to_add):
	quotient = 0
	for num in nums_to_add:
		if nums_to_add.index(num) == 0:
			quotient = num
		else:
			quotient = quotient / num
	return quotient

# libraries = ["console", "math", "string"]
libraries = {
	"console" : MhlLibrary(name="console", functions={"print":print_function}),
	"math" : MhlLibrary(name="math", functions=["add", "subtract", "multiply", "divide"]),
	"string" : MhlLibrary(name="string", functions={"print_string":print_function_string}),
}
librariesInScript = []

functions_in_script = {}

def access_library(library):
	global functions_in_script
	librariesInScript.append(library)
	funcs_to_add = {}
	for function in libraries[library].functions:
		funcs_to_add = funcs_to_add | {function:libraries[library].functions[function]}
	functions_in_script = functions_in_script | funcs_to_add

def create_variable_function(name, value, var_dict):
	global script_variables
	new_var_to_create = {}
	if value.isdigit():
		new_var_to_create = {name:int(value)}
	elif value == "true":
		new_var_to_create = {name:True}
	elif value == "false":
		new_var_to_create = {name:False}
	elif value.startswith('"') and value.endswith('"'):
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
		if word.startswith("//"): #For Comments
			continue
		elif word.startswith("var "): #To Declare Variables
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
		elif word.startswith("access library(") and word.endswith(")"): #To add a library to the script
			new_word = word.replace("access library(", "")
			new_word = new_word.replace(")", "")
			if new_word in libraries:
				access_library(new_word)
			else:
				LogErrors([f"There is no library with the name {new_word}"], (lines.index(word)+1))
				return
		elif "(" in word and ")" in word:
			new_word = word.replace(")", "")
			new_word = new_word.split("(")
			if new_word[0] in functions_in_script:
				functions_in_script[new_word[0]](new_word[1], (lines.index(word)+1))
			else:
				LogErrors([f"{new_word[0]} is not a valid function."], (lines.index(word)+1))
				return

parser()