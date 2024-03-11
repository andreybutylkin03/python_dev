import cmd

class Echoer(cmd.Cmd(completekey='tab'):
    """Dumb echo command REPL"""

    prompt = ">>"
    words = "one", "two", "three", "four", "five", "six"

    def do_echo(self, arg):
        print(arg)

    def complete_echo(self, text, line, begidx, endidx):
        print(text)
        return [c for c in self.words]

    def do_EOF(self, args):
        return True

if __name__ == "__main__":
    Echoer().cmdloop()
