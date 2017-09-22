import robot
r = robot.Robot()
from time import sleep

rs =30
ls =30
dis = 30
while 1:
  r.go_diff(rs,ls,1,1)
  if (r.read_sensor(2) < 40 and r.read_sensor(3) < 40):
    print("TRAP")
    r.stop()
    r.go_diff(rs,ls,0,1)
    sleep(4)
    r.stop()
  if (r.read_sensor(0) < dis):
    r.stop()
    if (r.read_sensor(2) > r.read_sensor(3)):
      print("Lige ud fuck venstre bedst")
      r.go_diff(rs,ls,0,1)
      sleep(0.5)
      r.stop()
    else:
      print("Lige ud fuck hojre bedst")
      r.go_diff(rs,ls,1,0)
      sleep(0.5)
      r.stop()
  if (r.read_sensor(2) < dis):
    print("venstre tight drej")
    r.go_diff(rs,ls,1,0)
    sleep(0.5)
    r.stop()
  if (r.read_sensor(3) < dis):
    print("hojre tight drej")
    r.go_diff(rs,ls,0,1)
    sleep(0.5)
    r.stop()
