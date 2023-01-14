from selenium import webdriver
import pyautogui
import time
from selenium.webdriver.chrome.options import Options
import pyperclip
import logging
import sys

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
        logging.info("[Pybricks] Loaded https://code.pybricks.com/")

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
        logging.info("[Pybricks] File \"MazeRunner\" Created")

    def runprogram(self):
        # print(pyautogui.screenshot().getpixel((558, 216)))
        while True:
            if pyautogui.screenshot().getpixel((558, 216)) != (117, 186, 223):
                pyautogui.press("F5") # runprogram if option is available
                break
        
        # Logging
        logging.info("[Pybricks] Executed File \"MazeRunner\"")
    
    def stopprogram(self):
        # print(pyautogui.screenshot().getpixel((637, 220)))
        while True:
            if pyautogui.screenshot().getpixel((637, 220)) != (117, 186, 223):
                pyautogui.press("F6") # stopprogram if option is available
                break
        
        logging.info("[Pybricks] Program Interrupted")
    
    def copyfrfile(self, path):
        infile = open(path, "r")
        lines = infile.readlines()

        txt = ""

        for line in lines:
            txt += line

        pyperclip.copy(txt)
        pyautogui.hotkey("ctrl", "v")

    def initalise(self):

        # Go to text line
        pyautogui.click(457, 317) # Clicking on the space beside the first line
        self.load()

        # Writing init file
        self.copyfrfile(self.PATH_TO_INIT)

    def runcmd(self):
        self.writecmd()
        self.runprogram()

    def Isprogramrunning(self):
        if pyautogui.screenshot().getpixel((558, 216)) == (117, 186, 223): # Option is unavailable
            return True 
        else:
            return False
            
    def exit(self, check = False):

        # For testing check
        if check:
            self.load(timeout = 1)
            while self.Isprogramrunning():
                pass

        # Deleting the file
        pyautogui.click(341, 208)
        self.load(timeout= 0.30)
        pyautogui.click(1140, 598)
        self.load()
        self.hidewindow()

    def writecmd(self):

        self.showwindow()
        self.load(timeout = 0.3)

        # Go to text line
        self.createnewfile()

        # Writing init file
        self.initalise()

        # Writing cmd file
        self.copyfrfile(self.PATH_TO_CMD)
        self.load(timeout = 0.3)
    
    def connectspike(self):
        
        # Interacting with pop-up bluetooth selection
        pyautogui.click(431, 197)
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
        logging.info("[Pybricks] Connecting to Hub...")
        # print("Hub Found")

        pyautogui.click(543, 593) # Click on "pair"
        self.load(timeout = 3)
        pyautogui.moveTo(1350, 1047)

        # if pyautogui.screenshot().getpixel((434, 175)) == (255, 255, 255):
        #     self.connectspike()
    
    def closewindow(self):
        self.driver.quit()

    def showwindow(self):
        if not self.show_hide:
            pyautogui.click(1350, 1047)
            self.show_hide = True

    def hidewindow(self):
        if self.show_hide:
            pyautogui.click(1350, 1047)
            self.show_hide = False
    
    def reload(self):
        self.driver.refresh()

    def exec(self):
        self.start()

        # navigating the menu
        self.navigatetodocs()

        # Connect to spikeprime
        self.connectspike()# To ensure that the spike prime is connected 

        logging.info("[Pybricks] Hub Connected.")

        # Hide Window
        self.hidewindow()

if __name__ == "__main__":
    # Logging
    file_handler = logging.FileHandler(filename=r"C:\Users\harry\Desktop\SH Robotics\2023-SH-Open-House\runMazerobot\logs.txt",mode="a")
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.INFO, handlers=handlers)

    # Pybricks instance
    pyb = autopybricks()

    # Execution(s)
    for i in range(3):
        pyb.writecmd()
        pyb.runprogram()
        pyb.exit(check = True)

    pyb.closewindow()
    # End Log 
    logging.info("[Local] Session Ended \n\n")
