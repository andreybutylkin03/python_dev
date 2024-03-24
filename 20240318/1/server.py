from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import sys
import shlex
import cmd
import readline
import rlcompleter
import asyncio


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


async def echo(reader, writer):
    area = Area()

    while data := await reader.readline():
        print(data)
        writer.write(data.swapcase())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":    
    asyncio.run(main())
