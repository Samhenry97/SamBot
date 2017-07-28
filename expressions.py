import re

class Node:
	def __init__(self, c, left=None, right=None):
		self.c = c
		self.left = left
		self.right = right

	def __repr__(self):
		if self.left is None or self.right is None:
			return self.c
		return '{0}({1},{2})'.format(self.c, self.left, self.right)

class ExpressionTree:
	def __init__(self, postfix):
		self.postfix = postfix
		self.root = None
		self.stack = []
		self._setup()

	def _setup(self):
		reFloat = re.compile('[0-9]*\.?[0-9]+')
		for s in self.postfix.split():
			while s != '':
				loc = [m.span() for m in reFloat.finditer(s)]
				if len(loc) > 0 and loc[0][0] == 0: # Number at beginning
					num = s[:loc[0][1]]
					self.stack.append(Node(num))
					s = s[loc[0][1]:]
				elif s[0] in '*/+-%^':
					if len(self.stack) < 2:
						raise RuntimeError('Could not generate expression tree.')
					right = self.stack.pop()
					left = self.stack.pop()
					self.stack.append(Node(s[0], left, right))
					s = s[1:]
				else:
					raise RuntimeError('Could not parse expression tree.')

		if len(self.stack) != 1:
			raise RuntimeError('Could not get root for postfix expression.')
		self.root = self.stack.pop()

	def _eval(self, node):
		if node.left is None or node.right is None:
			return float(node.c)
		if node.c == '*':	return self._eval(node.left) * self._eval(node.right)
		elif node.c == '/': return self._eval(node.left) / self._eval(node.right)
		elif node.c == '+': return self._eval(node.left) + self._eval(node.right)
		elif node.c == '-': return self._eval(node.left) - self._eval(node.right)
		elif node.c == '%': return self._eval(node.left) % self._eval(node.right)
		elif node.c == '^': return self._eval(node.left) ** self._eval(node.right)
		else: raise RuntimeError('Unknown operator: ' + c)

	def eval(self):
		return self._eval(self.root)

class InfixToPostfix:
	def __init__(self, infix):
		self.infix = infix
		self.stack = []
		self.stream = []

	def genPostfix(self):
		reFloat = re.compile('[0-9]*\.?[0-9]+')
		for s in self.infix.split():
			while s != '':
				loc = [m.span() for m in reFloat.finditer(s)]
				if len(loc) > 0 and loc[0][0] == 0: # Number at beginning
					num = s[:loc[0][1]]
					self.stream.append(num)
					s = s[loc[0][1]:]
				elif s[0] in '*/+-%^()':
					c = s[0]
					if c == '+' or c == '-':
						while len(self.stack) != 0 and self.stack[-1] != '(':
							self.stream.append(self.stack.pop())
						self.stack.append(c)
					elif c == '^' or c == '(':
						self.stack.append(c)
					elif c == ')':
						while len(self.stack) != 0 and self.stack[-1] != '(':
							self.stream.append(self.stack.pop())
						if len(self.stack) == 0:
							raise RuntimeError('Mismatched Parentheses')
						elif self.stack[-1] == '(':
							self.stack.pop()
					elif c == '*' or c == '/' or c == '%':
						while len(self.stack) != 0 and not (self.stack[-1] != '+' or self.stack[-1] != '-'):
							self.stream.append(self.stack.pop())
						self.stack.append(c)
					else:
						raise RuntimeError('Unknown Operator in Infix')
					s = s[1:]
				else:
					raise RuntimeError('Could not parse expression tree.')

		while len(self.stack) != 0 and self.stack[-1] != '(':
			self.stream.append(self.stack.pop())

		return ' '.join(self.stream)


class ExpressionSolver:
	def __init__(self, infix):
		self.infix = infix
		self.postfix = ''

	def solve(self):
		self.postfix = self.infixToPostfix()
		return self.postfixSolve()

	def infixToPostfix(self):
		return InfixToPostfix(self.infix).genPostfix()

	def postfixSolve(self):
		return ExpressionTree(self.postfix).eval()

if __name__ == '__main__':
	n1 = Node('3')
	n2 = Node('5')
	n3 = Node('+', n1, n2)
	print(n3)

	i = InfixToPostfix('3 + (4 - 2)')
	print(i.genPostfix())

	t = ExpressionTree('-3.0 4.0 *')
	print(t.eval())

	e = ExpressionSolver('-3.00 + (4 - 2)')
	print(e.solve())

	ans = input()
	while ans != 'quit':
		e = ExpressionSolver(ans)
		print(e.solve())
		ans = input()
