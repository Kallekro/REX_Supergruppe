import robot
r = robot.Robot()

def getchar():
    #Returns a single character from standard input
    import tty, termios, sys
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


rs = 79 
ls = 80
on = True
while on:
    ch = ord(getchar())
    if (ch == 119): #w
        print r.go_diff(ls,rs,1,1)
    elif (ch == 97): #a
        print r.go_diff(ls,rs,0,1)
    elif (ch == 115): #s
        print r.go_diff(ls,rs,0,0)
    elif (ch == 100): #d
        print r.go_diff(ls,rs,1,0)
    elif (ch == 50):
        rs += 10
        ls += 10
    elif (ch == 49):
        rs -= 10
        ls -= 10
    elif (ch == 113):
        print r.stop()
    elif (ch == 122):
        print r.stop()
        on = False
