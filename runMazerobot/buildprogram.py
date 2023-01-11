class Builder():
    def __init__(self):

        # Constants
        self.speed = 30
        self.turn_spd = 30

        # File Path
        self.PATH_TO_CMD = "C:\\Users\\harry\\Desktop\\SH Robotics\\2023-SH-Open-House\\runMazerobot\\cmd.txt"

    def buildrobotcmd(self, commands):
        
        # Make sure that the command is in the right format [...]
        if commands.find("[") == -1 or commands.find("]") == -1:
            raise ValueError("Invalid Robot Commands")

        # Opening outFile
        self.outFile = open(self.PATH_TO_CMD, "w")

        # Reformatting commands & breaking into list of commands
        commandlist = commands.replace("[", "").replace("]", "").split(",")

        # Writing to cmd file
        for command in commandlist:

            try: 
                m = command[0]
                if m != "lt":
                    v = int(command[1 :])
                else:
                    m = command[ : 2]
                    v = int(command[2 : ])
            except:
                print(f"\"{command}\" is invalid")
                continue
            # print(m, v)

            # Basic Movements
            if m == "f":
                self.f(v)

            elif m == "b":
                self.b(v)

            elif m == "l":
                self.l(v)

            elif m == "r":
                self.r(v)
            
            # Gyro Movement
            # elif m == "gf":
            #     self.gf(v)
            # elif m == "gt":
            #     self.gt(v)

            # Line Tracing
            elif m == "lt":
                self.lt(v)
        
        # Closing File
        self.outFile.close()

    # Basic Movements
    def r(self, turn_angle):
        self.outFile.writelines(f"pair.turn({-(turn_angle/360 * 1325)}) \n")
        # print(f"pair.turn(speed = {turn_angle}) \n")

    def l(self, turn_angle):
        self.outFile.writelines(f"pair.turn({turn_angle/360 * 1325}) \n")
        # print(f"pair.turn(speed = {-turn_angle}) \n")

    def f(self, deg):
        self.outFile.writelines(f"pair.straight({deg}) \n")
        # print(f"pair.straight({deg}) \n")

    def b(self, deg):
        self.outFile.writelines(f"pair.straight({-deg}) \n")
        # print(f"pair.straight({-deg}) \n")
    
    # Gyro
    # def gf(self, deg):
    #     self.outFile.writelines(f"gyro_straight({self.speed}, {deg}, target = 0, forward = True) \n")

    # def gt(self, bearing):
    #     self.outFile.writelines(f"gyro_turn({bearing}, 2, speed = {self.speed}, timeout = False, steering = 100) \n")

    # Line-Tracing
    def lt(self, deg):
        self.outFile.wrtielines(f"line_trace({deg}) \n")

if __name__ == "__main__":
    b = Builder()
    b.buildrobotcmd("[f80,r90,b100,l100,gf2000]") # Test Case