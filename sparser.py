L_LETTERS = "abcdefghijklmnopqrstuvwxyz"
U_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
ALL_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPERATORS = L_LETTERS + U_LETTERS + "+*/-"
WHITESPACE = " \t"


def split_into_st(program): # split_into_st("apple") # ['a', 'p', 'p', 'l', 'e']
	result = []
	char_index = 0
	token_type = 0 # 0 is none, 1 is .op, 2 is num, I'll think of more later
	# actually, for that matter, what other types are there?
	token = ""

	while char_index < len(program):
		char = program[char_index]
		print(char, token_type)
		if token_type == 0:
			if char in WHITESPACE:
				result.append(token)
				token = ""
				token_type = 0
			if char in OPERATORS:
				token += char
				result.append(token)
				token = ""
				token_type = 0
			if char == ".":
				token += "."
				token_type = 1
		elif token_type == 1:
			token += char
			print(token)
			result.append(token)
			token = ""
			token_type = 0
		elif token_type == 2:
			pass
		char_index += 1
	return result


def a():
	print("hi")