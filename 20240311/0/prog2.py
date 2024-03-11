import calendar
import cmd

class Cal(cmd.Cmd):
    prompt = ">>"

    def do_prmonth(self, arg): 
        match arg.split():
            case [theyear, themonth]:
                print(theyear, themonth)
                calendar.TextCalendar().prmonth(int(theyear), int(themonth))

    def do_pryear(self, arg):
        match arg.split():
            case [theyear]:
                calendar.TextCalendar().pryear(int(theyear))

    def do_EOF(self, arg):
        return True

if __name__ == "__main__":
    Cal().cmdloop()
