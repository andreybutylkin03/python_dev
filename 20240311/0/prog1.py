import cmd

class Echoer(cmd.Cmd):
    """Dumb echo command REPL"""

    prompt = ">>"

    def do_echo(self, arg):
        print(arg)

    def do_EOF(self, args):
        return True

if __name__ == "__main__":
    Echoer().cmdloop()
