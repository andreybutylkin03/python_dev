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
        self.weapon = {'sword':10, 'spear':15, 'axe':20}


    async def moved_to(self, x, y, writer, reader):
        self.pers.move_x(x)
        self.pers.move_y(y)

        writer.write(f"Moved to ({self.pers.x}, {self.pers.y})\n".encode())
        await reader.readline()

        self.encounter(self.pers.x, self.pers.y, writer)


    async def addmon(self, x, y, hi, name, hp, writer, reader):
        if name not in list_cows() and name != "jgsbat":
            writer.write("Cannot add unknown monster\n".encode())
            return 

        vr_monster = self.monster[x][y]

        self.monster[x][y] = Monster(x, y, hi, name, hp)
        
        writer.write(f"Added monster {name} to ({x}, {y}) saying {hi}\n".encode())
        await reader.readline()

        if vr_monster is not None:
            writer.write("Replaced the old monster\n".encode())
        else:
            writer.write("\n".encode())


    def encounter(self, x, y, writer):
        if self.monster[x][y] is not None:
            writer.write(f"{self.monster[x][y].name} {self.monster[x][y].text}\n".encode())
        else:
            writer.write("nomonster\n".encode())


    async def attack(self, monster_name, weapon, writer, reader):
        if self.monster[self.pers.x][self.pers.y] is None:
            writer.write("No monster here\n".encode())
        else:
            damag = weapon

            vr_hp = self.monster[self.pers.x][self.pers.y].hp
            vr_name = self.monster[self.pers.x][self.pers.y].name

            if monster_name != vr_name:
                writer.write(f"No {monster_name} here\n".encode())
                return
            
            if vr_hp > damag:
                self.monster[self.pers.x][self.pers.y].hp -= damag
                vr_hp = damag
            else:
                self.monster[self.pers.x][self.pers.y] = None

            writer.write(f"Attacked {vr_name}, damage {vr_hp} hp\n".encode())
            await reader.readline()

            if self.monster[self.pers.x][self.pers.y] is None:
                writer.write(f"{vr_name} died\n".encode())
            else:
                writer.write(f"{vr_name} now has {self.monster[self.pers.x][self.pers.y].hp}\n".encode())


async def echo(reader, writer):
    area = Area()

    while data := await reader.readline():
        data = data.decode()
        
        s = shlex.split(data, False, False)

        match s:
            case ['move', x, y]:
                await area.moved_to(int(x), int(y), writer, reader)
            case ['addmon', x, y, hello_string, monster_name, hp]:
                await area.addmon(int(x), int(y), hello_string, monster_name, int(hp), writer, reader)
            case ['attack', monster_name, 'with', weapon]:
                await area.attack(monster_name, int(weapon), writer, reader)

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":    
    asyncio.run(main())
