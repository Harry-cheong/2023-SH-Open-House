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

    # Finding keyword, separators in cmd
    def find(self, _keyword, separator, incmd, statement_list, nested = False):
        #TODO Implement keyword arg nested
        
        keyword = _keyword + separator # e.g. if + ^ to form "if^"
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

            # parsing gen cmds 
            if not nested:
                if statement[1].find(",") != -1:
                    for i in statement[1].split(","):
                        statement.append(i)
                    del statement[1]
            # print(incmd)

            else:
                # print(statement[1])
                statement[1], statement= self.findifelse(statement[1], statement, ifkey = "inf", elifkey = "enf", elsekey = "enl")
 
                for cmd in statement:
                    print(cmd)
                    icmd = statement.index(cmd)

                    # parsing gen cmds inside nested loops into indv cmds
                    if cmd != _keyword and type(cmd) == str:
                        if statement[icmd].find(",") != -1:
                            # print(statement[icmd].split(","))
                            for i in statement[icmd].split(","):
                                if i != "": 
                                    del statement[icmd]
                                    statement.insert(icmd, i)

                    # merging nested loops back into the statement
                    elif type(cmd) == list:
                        statement.insert(statement[icmd][1] + 1, statement[icmd][0])
                        statement.remove(cmd)
                                    
                
                # print(statement)

            # Appending it to statement
            statement_list.append([statement, cmdpos])
            # print(incmd, statement_list)

            return incmd, statement_list, True

    def findifelse(self, commands, statement_list, ifkey = "if", elifkey = "ef", elsekey = "el"):
        status = True
        while True:
            if status:
                commands, statement_list, status = self.find(ifkey, "^", commands, statement_list)
                if status:
                    commands, statement_list, status = self.find(elifkey, "^", commands, statement_list)
                
                if status:
                    commands, statement_list, status = self.find(elsekey, "^", commands, statement_list)
            else:
                break
        return commands, statement_list

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
        
        if type(command) is not list:
            print(f"{command} Invalid")

        if command[0] == "if" or command[0] == "inf":
            # print(command)
            self.buildcondition(command[1])
            self.outFile.writelines(f"{self.lstr}if " + self.buildcondition(command[1]) + ":\n")
            self.cglobalindent(1)

            for i in range(2, len(command)):
                # print(command[i])
                self.buildgencmds(command[i])
            self.cglobalindent(-1)

        elif command[0] == "ef" or command[0] == "enf":
            self.outFile.writelines(f"{self.lstr}elif " + self.buildcondition(command[1]) + ":\n")
            self.cglobalindent(1)

            for i in range(2, len(command)):
                self.buildgencmds(command[i])
            self.cglobalindent(-1)

        elif command[0] == "el" or command[0] == "enl":
            self.outFile.writelines(f"{self.lstr}else:\n")
            self.cglobalindent(1)

            for i in range(1, len(command)):
                self.buildgencmds(command[i])
            self.cglobalindent(-1)

        elif command[0] == "w":
            self.outFile.writelines(f"{self.lstr}while True:\n")
            self.cglobalindent(1)
            
            for i in range(1, len(command)):
                if type(command[i]) is list: 
                    self.buildlogiccmd(command[i])
                else: self.buildgencmds(command[i])
            self.cglobalindent(-1)
        
        elif command[0] == "for": 
            self.outFile.writelines(f"{self.lstr}for i in range({command[1]}):\n")
            self.cglobalindent(1)

            for i in range(2, len(command)):
                if type(command[i]) is list: 
                    self.buildlogiccmd(command[i])
                else: self.buildgencmds(command[i])

            self.cglobalindent(-1)

    def buildgencmds(self, command):
        
        # Special case : kb
        if command[:2] == "kb":
            self.outFile.writelines(f"{self.lstr}break\n")
            return

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

    def buildcmds(self, _commands):
        
        # Copy of og cmds
        commands = _commands

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
        print("\n Commands: " + commands + "\n") # the original cmds passed into the fn
        commands, statement_list, = self.findifelse(commands, statement_list)
        commands, statement_list, status = self.find("w", "|", commands, statement_list, nested = False)
        commands, statement_list, status = self.find("for", "|", commands, statement_list, nested = False)
        #TODO Nested statements

        # Splitting norm commands into indiv cmds
        # print(scommands)
        ic = commands.count(",") + 1
        command_list = commands.split(",")

        # Removing empty strs in the command_list
        while True:
            try:
                command_list.remove("")
            except:
                break
        
        # Fix index of nested loops:

        # Findin the index of the while statement in statement_list

        # Merging statement_list into command_list
        for i in range(ic):
            for statement in statement_list:
                if statement[1] == i:
                    command_list.insert(statement[1], statement[0])
        print(statement_list, "\n")
        print(command_list, "\n")

        # Writing to cmd file
        for command in command_list:
            if type(command) is list:
                # print(command)
                self.buildlogiccmd(command)
  
            else:
                self.buildgencmds(command)
        
        # Closing File
        self.outFile.close()

        # Logging
        try: logging.info(f"[Builder] Built {_commands}")
        except: pass
        
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
    b.buildcmds("[w|inf^lr<50,r10^,inf^lr<100,l10^|]") # Test Case
    # print("if " + b.buildcondition("us>300") + ": \n")