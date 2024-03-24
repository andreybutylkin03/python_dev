from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import sys
import shlex
import cmd
import readline
import rlcompleter
import socket

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

class MonsterConst():
    def __init__(self):
        self.cow = read_dot_cow(StringIO("""
        $the_cow = <<EOC;
            ,_                    _,
            ) '-._  ,_    _,  _.-' (
            )  _.-'.|\\\0\\--//|.'-._  (
             )'   .'\\/o\\/o\\/'.   `(
              ) .' . \\====/ . '. (
               )  / <<    >> \\  (
                '-._/``  ``\\_.-'
          jgs     __\\\0\\'--'//__
                 (((""`  `"")))
        EOC
        """))


class InterGame(cmd.Cmd):
    prompt = ''
    weapon = {'sword':10, 'spear':15, 'axe':20}
    name_of_monster = list_cows() + ["jgsbat"]

    host = "localhost"
    port = 1337
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))


    def default(self, args):
        print("Invalid command")


    def pr_mon(self, name, text):
        if name == "jgsbat":
            return cowsay(text, cowfile=MonsterConst().cow)
        else:
            return cowsay(text, cow=name)

    def do_up(self, args):
        self.s.sendall("move 0 1\n".encode())
        ot = self.s.recv(1024).rstrip().decode()
        print(ot)
        self.s.sendall("\n".encode())

        ot = shlex.split(self.s.recv(1024).rstrip().decode())
        if len(ot) == 2:
            print(self.pr_mon(ot[0], ot[1]))


    def do_down(self, args):
        self.s.sendall("move 0 -1\n".encode())
        ot = self.s.recv(1024).rstrip().decode()
        print(ot)
        self.s.sendall("\n".encode())

        ot = shlex.split(self.s.recv(1024).rstrip().decode())
        if len(ot) == 2:
            print(self.pr_mon(ot[0], ot[1]))


    def do_left(self, args):
        self.s.sendall("move -1 0\n".encode())
        ot = self.s.recv(1024).rstrip().decode()
        print(ot)
        self.s.sendall("\n".encode())

        ot = shlex.split(self.s.recv(1024).rstrip().decode())
        if len(ot) == 2:
            print(self.pr_mon(ot[0], ot[1]))



    def do_right(self, args):
        self.s.sendall("move 1 0\n".encode())
        ot = self.s.recv(1024).rstrip().decode()
        print(ot)
        self.s.sendall("\n".encode())

        ot = shlex.split(self.s.recv(1024).rstrip().decode())
        if len(ot) == 2:
            print(self.pr_mon(ot[0], ot[1]))


    def do_addmon(self, args):
        a = shlex.split(args, False, False)
        monster_name, hello_string, hitpoints, x, y = '', '', 0, 0, 0
        h_id, hit_id, x_id, y_id = [-1] * 4
        fl = [False] * 3
        m_id = 28
        for i in range(len(a) - 1):
            if a[i] == 'hello' and a[i + 1][0] == '"' or a[i + 1][0] == "'":
                h_id = i + 1
                m_id -= (i + i + 1)
                fl[0] = True
            elif a[i] == 'hp':
                hit_id = i + 1
                m_id -= (i + i + 1)
                fl[1] = True
            elif a[i] == 'coords' and i != len(a) - 2:
                x_id = i + 1
                y_id = i + 2
                m_id -= (i + i + 1 + i + 2)
                fl[2] = True
        
        if not all(fl):
            print(h_id, hit_id, x_id, y_id)
            print("Invalid command")
            return

        monster_name = a[m_id]
        hello_string = a[h_id]
        hitpoints = a[hit_id]
        x = a[x_id]
        y = a[y_id]

        try:
            x = int(a[x_id])
            y = int(a[y_id])
            hitpoints = int(a[hit_id])

            if not (0 <= x <= 9):
                raise TypeError
            if not (0 <= y <= 9):
                raise TypeError
            if hitpoints <= 0:
                raise TypeError

            self.s.sendall(f"addmon {x} {y} {hello_string} {monster_name} {hitpoints}\n".encode())
            vrr = self.s.recv(1024).rstrip().decode()
            print(vrr)
            if vrr != 'C':
                self.s.sendall("\n".encode())
                if (vrr := self.s.recv(1024).rstrip().decode()) and (vrr[0] == 'R'):
                    print(vrr)
        except Exception as ex:
            print("Invalid arguments")


    def do_attack(self, args):
        a = shlex.split(args, False, False)
        damag = 10

        monster_name = a[0]

        if len(a) > 2 and a[1] == 'with' and a[2] in {'sword', 'spear', 'axe'}:
            damag = self.weapon[a[2]]
        elif len(a) >= 2 and a[1] == 'with':
            print("Unknown weapon")
            return

        self.s.sendall(f"attack {monster_name} with {damag}\n".encode())
        vrr = self.s.recv(1024).rstrip().decode()
        print(vrr)
        if vrr[0] != 'N':
            self.s.sendall("\n".encode())
            print(self.s.recv(1024).rstrip().decode())


    def complete_attack(self, text, line, begidx, endidx):
        a = shlex.split(line[:begidx], False, False)

        if a[-1] == 'with':
            return [c for c in self.weapon if c.startswith(text)]
        elif a[-1] == 'attack':
            return [c for c in self.name_of_monster if c.startswith(text)]


    def do_EOF(self, args):
        self.s.sendall("\0".encode())
        self.s.close()
        print()
        return True


if __name__ == "__main__":
    print("<<< Welcome to Python-MUD 0.1 >>>")
    InterGame().cmdloop()
