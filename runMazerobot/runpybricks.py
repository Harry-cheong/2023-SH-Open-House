from selenium import webdriver
import pyautogui
import time
from selenium.webdriver.chrome.options import Options
import threading

class autopybricks():
    def __init__(self):
        self.PATH_TO_CMD = "C:\\Users\\harry\\Desktop\\SH Robotics\\2023-SH-Open-House\\runMazerobot\\cmd.txt"
        self.PATH_TO_INIT = "C:\\Users\\harry\\Desktop\\SH Robotics\\2023-SH-Open-House\\runMazerobot\\init.txt"
        self.show_hide = True
        self.exec()

    def start(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\harry\\Desktop\\Computing\\chromedriver.exe", options = chrome_options) 
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
        self.load(timeout = 0.30)

        # Config new file 

        # print(pyautogui.screenshot().getpixel((673, 542)))
        # when button is toggled on, pyautogui.screenshot()getpixel((688, 541)) = (197, 203, 211)
        if (pyautogui.screenshot().getpixel((674,536)) != (255, 255, 255)):
            pyautogui.click(674, 543) # Toggle template off if template if on
        self.load()


        pyautogui.click(678, 452) # Click into the text bar
        pyautogui.write("MazeRunner") # Name of file
        pyautogui.press("enter") # Confirm file
        self.load(timeout = 0.30)

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
        lines = infile.readlines()
        iline = 0

        c_indent = p_indent = 0

        for line in lines:
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
            time.sleep(0.08)

    def erasefile(self, path):
        infile = open(path, "r")
        lines = infile.readlines()
        iline = len(lines)

        for line in lines:
            for char in line:
                pyautogui.press("Backspace")
            # if iline != 1: pyautogui.press("Backspace")
            iline -= 1
        # pyautogui.press("enter")

    def initalise(self):

        # Go to text line
        pyautogui.click(457, 317) # Clicking on the space beside the first line

        # Writing init file
        self.copyfrfile(self.PATH_TO_INIT)

        # Resizing robot cmd txt box
        for i in range(15):
            pyautogui.press("enter")
        
        for i in range(16):
            pyautogui.press("backspace")
        pyautogui.press("enter")

    def runcmd(self):
        self.writecmd()
        self.runprogram()

    def exit(self):
        # TODO A thread to check the run button when it is blanked out, the program is running. 

        # Resetting
        self.erasefile(self.PATH_TO_CMD)
        self.hidewindow()

    def writecmd(self):

        self.showwindow()

        self.load(timeout = 0.3)
        # Go to text line
        pyautogui.click(454, 335) # Clicking on the right line

        # Writing cmd file
        self.copyfrfile(self.PATH_TO_CMD)
    
    def connectspike(self):
        
        # Interacting with pop-up bluetooth selection
        pyautogui.click(431, 197) # Click on bluetooth icon
        self.load(timeout = 0.30)

        # wait for "pybricks hub" to pop up and click on it
        # print(pyautogui.screenshot().getpixel((183, 180)))
        # print("Finding Hub")
        while True:
            # print(pyautogui.screenshot().getpixel((184, 170)))
            status = pyautogui.screenshot().getpixel((184, 170))
            if status == (117, 117, 117):    
                pyautogui.click(184, 170)
                break

        self.load()
        print("Hub Found")

        pyautogui.click(543, 593) # Click on "pair"
        self.load()
    
    def closewindow(self):
        self.driver.quit()

    def showwindow(self):
        if not self.show_hide:
            pyautogui.click(1330, 1047)
            self.show_hide = True

    def hidewindow(self):
        if self.show_hide:
            pyautogui.click(1330, 1047)
            self.show_hide = False
    
    def reload(self):
        self.driver.refresh()

    def checkterminal(self):
        pass

    def exec(self):
        self.start()

        # Creating a new file
        self.navigatetodocs()
        self.createnewfile()

        # Writing init file
        self.initalise()

        # Connect to spikeprime
        self.connectspike()

        # Hide Window
        self.hidewindow()

if __name__ == "__main__":
    pyb = autopybricks()
    pyb.writecmd()
    # pyb.closewindow()
    pyb.writecmd()
    # pyb.closewindow()
    # pyb.showwindow()
