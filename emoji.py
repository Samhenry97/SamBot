import random

happy = [0x1f601, 0x1f603, 0x1f604, 0x1f60a, 0x1f60c, 0x1f600, 0x263a]
funny = [0x1f602, 0x1f605, 0x1f61c, 0x1f61d, 0x1f60b, 0x1f61b]
sad =   [0x1f613, 0x1f614, 0x1f61e, 0x1f622, 0x1f623, 0x1f625]
mad =   [0x1f620, 0x1f621, 0x1f624]
tired = [0x1f634, 0x1f4a4]
cool =  [0x1f60e, 0x1f608]

def choice(list, min=1, max=1):
	ans = []
	for i in range(random.randint(min, max)):
		ans.append(chr(random.choice(list)))
	return ''.join(ans)

class Emoji:
	def happy(min=1, max=1):
		return choice(happy, min, max)

	def funny(min=1, max=1):
		return choice(funny, min, max)

	def sad(min=1, max=1):
		return choice(sad, min, max)

	def mad(min=1, max=1):
		return choice(mad, min, max)

	def tired(min=1, max=1):
		return choice(tired, min, max)

	def cool(min=1, max=1):
		return choice(cool, min, max)

	def poop(min=1, max=1):
		return chr(0x1F4A9) * random.randint(min, max)

	def get(type, min=1, max=1):
		if min > max:
			max = min
			
		method = getattr(Emoji, type)
		return method(min, max)