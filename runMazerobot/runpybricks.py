from selenium import webdriver
import pyautogui
import time
from selenium.webdriver.chrome.options import Options

class autopybricks():
    def __init__(self):
        self.PATH_TO_CMD = "C:\\Users\\harry\\Desktop\\SH Robotics\\2023-SH-Open-House\\runMazerobot\\cmd.txt"
        self.PATH_TO_INIT = "C:\\Users\\harry\\Desktop\\SH Robotics\\2023-SH-Open-House\\runMazerobot\\init.txt"

    def start(self):
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\harry\\Desktop\\Computing\\chromedriver.exe") 
        self.driver.maximize_window()
        self.driver.get("https://code.pybricks.com/")
        self.load(timeout = 0.3)

    def load(self, timeout = 0.2):
        time.sleep(timeout)

    def navigatetodocs(self):
        pyautogui.click(456, 490) # Exit tutorial mode
        self.load()
        pyautogui.click(23,169) # Click on doc menu
        self.load()
    
    def createnewfile(self):
        
        # Click on "+" icon
        pyautogui.click(343,166)
        self.load(timeout = 0.20)

        # Config new file 

        # print(pyautogui.screenshot().getpixel((673, 542)))
        # when button is toggled on, pyautogui.screenshot()getpixel((688, 541)) = (197, 203, 211)
        if (pyautogui.screenshot().getpixel((674,543)) == (234, 236, 241)):
            pyautogui.click(674, 543) # Toggle template off if template if on
        self.load()
        pyautogui.click(678, 452) # Click into the text bar
        pyautogui.write("MazeRunner") # Name of file
        pyautogui.press("enter") # Confirm file
        self.load()

    def runprogram(self):
        # print(pyautogui.screenshot().getpixel((558, 216)))
        while True:
            if pyautogui.screenshot().getpixel((558, 216)) != (117, 186, 223):
                pyautogui.press("F5") # runprogram if option is available
                break
    
    def stopprogram(self):
        # print(pyautogui.screenshot().getpixel((637, 220)))
        while True:
            if pyautogui.screenshot().getpixel((637, 220)) != (117, 186, 223):
                pyautogui.press("F6") # runprogram if option is available
                break
    
    def copyfrfile(self, path):
        infile = open(path, "r")
        init = infile.readlines()
        iline = 0

        c_indent = p_indent = 0

        for line in init:
            iline += 1

            # To avoid: blank line is len0.25, thus round to 0
            c_indent = round((len(line) - len(line.lstrip()))/4)
            # print(f"{iline} : {c_indent}, {p_indent}")

            # Writing line
            if line == "\n":
                pyautogui.press("enter")

            else:
                # Fixing Indentation
                if c_indent < p_indent:
                    if (p_indent - c_indent) == 1:
                        pyautogui.press("Backspace")
                    else:
                        for i in range(0, (p_indent - c_indent)):
                            pyautogui.press("Backspace")
                pyautogui.write(line.lstrip())

                # Updating prev indent num
                if c_indent != p_indent:
                    p_indent = c_indent

    def writetofile(self):

        # Go to text line
        self.load()
        pyautogui.click(457, 317) # Clicking on the space beside the first line

        # Writing init file
        self.copyfrfile(self.PATH_TO_INIT)

        # Writing cmd file
        self.copyfrfile(self.PATH_TO_CMD)
    
    def connectspike(self):
        
        #TODO: Check before connection
        
        # Interacting with pop-up bluetooth selection
        pyautogui.click(431, 197) # Click on bluetooth icon
        self.load(timeout = 0.30)

        pyautogui.click(246, 172) # click on "pybricks hub"
        self.load()

        pyautogui.click(543, 593) # Clikc on "pair"
        self.load(timeout = 0.50)
    
    def exec(self):
        self.start()
        self.navigatetodocs()
        self.createnewfile()
        # self.connectspike()
        self.writetofile()
        # self.runprogram()

        time.sleep(5)

        # Ending Program
        self.driver.quit()

if __name__ == "__main__":
    pyb = autopybricks()
    pyb.exec()
