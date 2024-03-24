from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import sys
import shlex
import cmd
import readline
import rlcompleter

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


class InterGame(cmd.Cmd):
    prompt = ''
    weapon = {'sword':10, 'spear':15, 'axe':20}
    name_of_monster = list_cows() + ["jgsbat"]


    def default(self, args):
        print("Invalid command")


    def do_up(self, args):
        pass


    def do_down(self, args):
        pass


    def do_left(self, args):
        pass


    def do_right(self, args):
        pass


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

        if monster_name not in name_of_monster:
            print("Cannot add unknown monster")
            return 

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

            #self.area.addmon(x, y, hello_string, monster_name, hitpoints)
        except:
            print("Invalid arguments")


    def do_attack(self, args):
        a = shlex.split(args, False, False)
        damag = 10

        monster_name = a[0]
        weapon_name = 'sword'

        if len(a) > 2 and a[1] == 'with':
            weapon_name = a[2]


    def complete_attack(self, text, line, begidx, endidx):
        a = shlex.split(line[:begidx], False, False)

        if a[-1] == 'with':
            return [c for c in self.weapon if c.startswith(text)]
        elif a[-1] == 'attack':
            return [c for c in self.name_of_monster if c.startswith(text)]


    def do_EOF(self, args):
        print()
        return True


if __name__ == "__main__":
    print("<<< Welcome to Python-MUD 0.1 >>>")
    InterGame().cmdloop()
