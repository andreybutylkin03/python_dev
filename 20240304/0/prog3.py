import shlex

s = input("ФИО: ")
p = input("МЕСТО: ")

print("register", shlex.join([s, p]))
