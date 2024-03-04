import shlex

s = input()
res = shlex.split(s)
print(shlex.join(res))
