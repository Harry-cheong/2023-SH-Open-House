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

    # Finding while, if, elif, else statements
    def find(self, keyword, separator, incmd, statement_list):
        #TODO Splitting inside while loop (implement exception when incmd is list type)
        # cmdislist = False

        # if type(incmd) is list:
        #     cmdislist = True
        #     for i in incmd:
        #         if incmd.find(keyword) != -1:
        #             incmd = i
        
        # if type(incmd) is not list:
        #     pass
        # else:
        #     return
        
        if incmd.find(keyword) == -1:
            return incmd, statement_list, False
                
        elif incmd.find(keyword) != -1:
            # print("Found")
            # Finding the statement
            i = incmd.find(keyword) # Find the keyword i.e. "if^"
            statement = incmd[i : incmd.find(separator, i + len(keyword)) + 1] # Slice the statement from the string
            cmdpos = incmd[ : i].count(",") # Determine the pos of the string if applicable
            
            # removing the sliced string fr incmds
            incmd = incmd[ : i] + incmd[incmd.find(separator, i + len(keyword)) + 1 : ]

            # parsing incmds into indiv cmds
            statement = statement.split(separator)
            statement.remove("")
            if statement[1].find(",") != -1:
                for i in statement[1].split(","):
                    statement.append(i)
                del statement[1]
            # print(incmd)

            # Appending it to statement
            statement_list.append([statement, cmdpos])
            # print(incmd, statement_list)

            return incmd, statement_list, True

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
        if ssor == "us":
            # print(f"us.distance() {comp} {value}")
            return (f"us.distance() {comp} {value}")
        elif ssor == "lr":
            # print(f"ls.reflections() {comp} {value}")
            return (f"ls.reflections() {comp} {value}")



    def buildlogiccmd(self, command):

        if type(command) is not list:
            print(f"{command} Invalid")

        if command[0] == "if":
            self.cglobalindent(1)
            self.outFile.writelines("if " + self.buildcondition(command[1]) + ": \n")
            for i in range(2, len(command)):
                self.buildrobotcmd(command[i])
            self.cglobalindent(-1)

        elif command[0] == "ef":
            self.cglobalindent(1)
            self.outFile.writelines("elif " + self.buildcondition(command[1]) + ": \n")
            for i in range(2, len(command)):
                self.buildrobotcmd(command[i])
            self.cglobalindent(-1)

        elif command[0] == "el":
            self.cglobalindent(1)
            self.outFile.writelines(f"else: \n")
            for i in range(1, len(command)):
                self.buildrobotcmd(command[i])
            self.cglobalindent(-1)

        elif command[0] == "w":
            self.cglobalindent(1)
            self.outFile.writelines(f"while True: \n")
            for i in range(1, len(command)):
                self.buildrobotcmd(command[i])
            self.cglobalindent(-1)
        
        elif command[0] == "for":
            self.cglobalindent(1)
            self.outFile.writelines(f"for i in range({command[1]}): \n")
            for i in range(2, len(command)):
                self.buildrobotcmd(command[i])
            self.cglobalindent(-1)

    def buildrobotcmd(self, command):
        
        # Writing robot cmds into file
        try: 
            m = command[0]
            v = int(command[1 :])

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

    def buildcmds(self, commands):
        
        # Make sure that the command is in the right format [...]
        if commands.find("[") == -1 or commands.find("]") == -1:
            raise ValueError("Invalid Robot Commands")

        # Opening outFile
        self.outFile = open(self.PATH_TO_CMD, "w")

        # Reformatting commands & breaking into list of commands
        statement_list = []

        # Removing outer brackets
        commands = commands.replace("[", "").replace("]", "")

        # Finding while, if, elif, else statements
        # print(commands)
        status = True
        while True:
            if status:
                commands, statement_list, status = self.find("if^", "^", commands, statement_list)
                commands, statement_list, status = self.find("ef^", "^", commands, statement_list)
                commands, statement_list, status = self.find("el^", "^", commands, statement_list)
            else:
                break
        commands, statement_list, status = self.find("for|", "|", commands, statement_list)
        commands, statement_list, status = self.find("w|", "|", commands, statement_list)

        #TODO Nested statements

        # Splitting norm commands into indiv cmds
        # print(commands)
        ic = commands.count(",") + 1
        command_list = commands.split(",")

        # Removing empty strs in the command_list
        while True:
            try:
                command_list.remove("")
            except:
                break

        # Merging statement_list into command_list
        for i in range(ic):
            for statement in statement_list:
                if statement[1] == i:
                    command_list.insert(statement[1], statement[0])
        # print(statement_list)
        print(command_list)

        # Writing to cmd file
        for command in command_list:
            if type(command) is list:
                # print(command)
                self.buildlogiccmd(command)
  
            else:
                self.buildrobotcmd(command)
        
        # Closing File
        self.outFile.close()

    # Basic Movements
    def r(self, turn_angle):
        self.outFile.writelines(f"{self.lstr}pair.turn({-(turn_angle/360 * 1325)}) \n")
        # print(f"pair.turn(speed = {turn_angle}) \n")

    def l(self, turn_angle):
        self.outFile.writelines(f"{self.lstr}pair.turn({turn_angle/360 * 1325}) \n")
        # print(f"pair.turn(speed = {-turn_angle}) \n")

    def f(self, deg):
        self.outFile.writelines(f"{self.lstr}pair.straight({deg}) \n")
        # print(f"pair.straight({deg}) \n")

    def b(self, deg):
        self.outFile.writelines(f"{self.lstr}pair.straight({-deg}) \n")
        # print(f"pair.straight({-deg}) \n")
    
    # Gyro
    # def gf(self, deg):
    #     self.outFile.writelines(f"gyro_straight({self.speed}, {deg}, target = 0, forward = True) \n")

    # def gt(self, bearing):
    #     self.outFile.writelines(f"gyro_turn({bearing}, 2, speed = {self.speed}, timeout = False, steering = 100) \n")

    # Line-Tracing
    def lt(self, deg):
        self.outFile.writelines(f"{self.lstr}line_trace({deg}) \n")

if __name__ == "__main__":
    b = Builder()
    b.buildcmds("[if^lr==10,r90^,ef^lr==30,l30^,el^r30^,f80,r90,if^us>300,r10^,b100,l100,w|f80|,t1000],for|2,f30|") # Test Case
    # print("if " + b.buildcondition("us>300") + ": \n")