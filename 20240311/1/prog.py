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


class Monster():
    def __init__(self, x, y, hi, name, hp):
        self.x = x
        self.y = y
        self.text = hi
        self.name = name
        self.jgsbat = MonsterConst().cow
        self.hp = hp


    def __str__(self):
        if self.name == "jgsbat":
            return cowsay(self.text, cowfile=self.jgsbat)
        else:
            return cowsay(self.text, cow=self.name)


class Pers():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def move_x(self, step):
        self.x += step
        
        if self.x == -1:
            self.x = 9
        elif self.x == 10:
            self.x = 0


    def move_y(self, step):
        self.y -= step

        if self.y == -1:
            self.y = 9
        elif self.y == 10:
            self.y = 0


class Area():
    def __init__(self):
        self.pers = Pers()
        self.monster = [[None for j in range(10)] for i in range(10)]


    def moved_to(self, direction):
        match direction:
            case 'up':
                self.pers.move_y(1)
            case 'down':
                self.pers.move_y(-1)
            case 'left':
                self.pers.move_x(-1)
            case 'right':
                self.pers.move_x(1)

        print(f"Moved to ({self.pers.x}, {self.pers.y})")

        self.encounter(self.pers.x, self.pers.y)


    def addmon(self, x, y, hi, name, hp):
        if name not in list_cows() and name != "jgsbat":
            print("Cannot add unknown monster")
            return 

        vr_monster = self.monster[x][y]

        self.monster[x][y] = Monster(x, y, hi, name, hp)
        
        print(f"Added monster {name} to ({x}, {y}) saying {hi}")

        if vr_monster is not None:
            print("Replaced the old monster")


    def encounter(self, x, y):
        if self.monster[x][y] is not None:
            print(self.monster[x][y])


class InterGame(cmd.Cmd):
    area = Area()
    prompt = ''


    def default(self, args):
        print("Invalid command")


    def do_up(self, args):
        self.area.moved_to('up')
 

    def do_down(self, args):
        self.area.moved_to('down')


    def do_left(self, args):
        self.area.moved_to('left')


    def do_right(self, args):
        self.area.moved_to('right')


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

            self.area.addmon(x, y, hello_string, monster_name, hitpoints)
        except:
            print("Invalid arguments")


    def do_attack(self, args):
        if self.area.monster[self.area.pers.x][self.area.pers.y] is None:
            print("No monster here")


    def do_EOF(self, args):
        return True


if __name__ == "__main__":
    print("<<< Welcome to Python-MUD 0.1 >>>")
    InterGame().cmdloop()
