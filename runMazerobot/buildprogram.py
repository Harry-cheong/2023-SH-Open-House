import logging

class Builder():
    def __init__(self):

        # Constants
        self.speed = 30
        self.turn_spd = 30

        # File Path
        self.PATH_TO_CMD = "C:\\Users\\harry\\Desktop\\SH Robotics\\2023-SH-Open-House\\runMazerobot\\cmd.txt"

        # outFile config
        self.indentation = 0
        self.lstr = ""

        # Special Characters
        self.indent = "    "

    def cglobalindent(self, i):
        self.indentation += i
        self.lstr = self.indentation * self.indent

    def buildcondition(self, condition):
        # Finding input
        ssor = condition[:2]

        # Finding num
        for char in condition:
            try:
                int(char)
                value = condition[condition.find(char) : ]
                break
            except:
                continue

        # Finding comparator
        comp = condition[2 : condition.find(char)]

        # print(ssor, value, comp)
        if ssor == "ud":
            # print(f"us.distance() {comp} {value}")
            return (f"us.distance() {comp} {value}")
        elif ssor == "lr":
            # print(f"ls.reflections() {comp} {value}")
            return (f"ls.reflection() {comp} {value}")



    def buildlogiccmd(self, command):
        
        # print(command)
        if command[:2] == "if":
            self.outFile.writelines(f"{self.lstr}if " + self.buildcondition(command[3:-1]) + ":\n")


        elif command[:2] == "ef":
            self.outFile.writelines(f"{self.lstr}elif " + self.buildcondition(command[3:-1]) + ":\n")

        elif command[:2] == "el":
            self.outFile.writelines(f"{self.lstr}else:\n")

        elif command[:2] == "wh":
            self.outFile.writelines(f"{self.lstr}while True:\n")
        
        elif command[:3] == "for": 
            self.outFile.writelines(f"{self.lstr}for i in range({command[4]}):\n")

    def buildgencmds(self, command):
        
        # Writing robot cmds into file
        try:
            m = command[0] # Movement Type 
            v = int(command[1 :]) # Value of perimeter

        except:
            print(f"\"{command}\" is invalid")
            return
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
        elif m == "t":
            self.lt(v)

    def buildcmds(self, _commands):
        
        # Copy of og cmds
        commands = _commands

        # Make sure that the command is in the right format [...]
        if commands.find("[") == -1 or commands.find("]") == -1:
            raise ValueError("Invalid Robot Commands")

        # Opening outFile
        self.outFile = open(self.PATH_TO_CMD, "w")

        # Removing outer brackets
        commands = commands[1:-1]

        # Splitting command
        command_list = commands.split(",")
        command_list.remove("")
        print(command_list)

        # Writing to cmd file
        for command in command_list:

            # Indentation
            if command == "[": 
                self.cglobalindent(1)
                continue
            elif command == "]": 
                self.cglobalindent(-1)
                continue

            # Special Case: 'break' keyword 
            if command[:2] == "kb":
                self.kb()
                continue
                
            # Figuring out whether command is logic/gencmd 
            if command.find('(') != -1:
                self.buildlogiccmd(command)
            else: 
                self.buildgencmds(command)
        
        # Closing File
        self.outFile.close()

        # Logging
        try: logging.info(f"[Builder] Built {_commands}")
        except: pass
    
    # 'break' keyword 
    def kb(self):
        self.outFile.writelines(f"{self.lstr}break\n")

    # Basic Movements
    def r(self, turn_angle):
        self.outFile.writelines(f"{self.lstr}pair.turn({-round(turn_angle/360 * 1325)})\n")
        # print(f"pair.turn(speed = {turn_angle}) \n")

    def l(self, turn_angle):
        self.outFile.writelines(f"{self.lstr}pair.turn({round(turn_angle/360 * 1325)})\n")
        # print(f"pair.turn(speed = {-turn_angle}) \n")

    def f(self, deg):
        self.outFile.writelines(f"{self.lstr}pair.straight({deg})\n")
        # print(f"pair.straight({deg}) \n")

    def b(self, deg):
        self.outFile.writelines(f"{self.lstr}pair.straight({-deg})\n")
        # print(f"pair.straight({-deg}) \n")
    
    # Gyro
    # def gf(self, deg):
    #     self.outFile.writelines(f"gyro_straight({self.speed}, {deg}, target = 0, forward = True) \n")

    # def gt(self, bearing):
    #     self.outFile.writelines(f"gyro_turn({bearing}, 2, speed = {self.speed}, timeout = False, steering = 100) \n")

    # Line-Tracing
    def lt(self, deg):
        self.outFile.writelines(f"{self.lstr}line_trace({deg})\n")

if __name__ == "__main__":
    b = Builder()
    b.buildcmds("[if(ud>1000),[,f100,l100,],r100,wh(),[,if(lr>50),[,l100,],ef(lr<30),[,r100,],],]") # Test Case
    # print("if " + b.buildcondition("us>300") + ": \n")