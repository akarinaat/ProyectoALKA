string_ops = "* / + - decfunc decvar < > != = param goto gotof call".split()

Operaciones = dict(zip(string_ops, range(len(string_ops))))
# {'*': 0, '/': 1, '+': 2, '-': 3, 'decfunc': 4, 'decvar': 5, '<': 6, '>': 7, '!=': 8, '=': 9, 'param': 10, 'goto': 11, 'gotof': 12, 'call': 13}
