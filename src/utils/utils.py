import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

class Utils(object):
    @staticmethod
    def load_page():
        driver = webdriver.Chrome()
        driver.get('https://www.chess.com/login')
        return driver

    @staticmethod
    def login(driver, username, password):
        elem = driver.find_element(By.ID,'username')
        elem.clear()
        elem.send_keys(username)
        elem = driver.find_element(By.ID,'password')
        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        return

    @staticmethod
    def play_game(driver):
        while driver.current_url != "https://www.chess.com/play/computer":
            driver.get('https://www.chess.com/play/computer')
        #style = str(board.get_attribute("style"))
        #a = style.find("height")
        #b = len(style)
        #size = float(style[a+8:b-3])
        #quad = size / 8
        #center = quad / 2   
        #test = board.execute(Command.FIND_CHILD_ELEMENTS)
        #print(len(test))
        while True:   
            actions = ActionChains(driver)
            board = driver.find_element(By.ID, "chessboard_boardarea")
            while len(driver.find_elements(By.CLASS_NAME, 'legal-move-hint')) > 0:
                driver.execute_script(""" 
                    var syshint = document.getElementsByClassName("legal-move-hint");
                    syshint[0].parentNode.removeChild(syshint[0]);
                """)
                time.sleep(0.1)
            board = driver.find_element(By.ID, "chessboard_boardarea")
            pecas = driver.find_elements(By.CLASS_NAME, "chess_com_piece") 
            #time.sleep(1)
            for i in range(len(pecas)):
                print(i+1)   
                try:      
                    actions.reset_actions()      
                    actions.click(pecas[i])
                    actions.perform()  
                    #time.sleep(0.7)
                    syshint = driver.find_elements(By.CLASS_NAME, 'legal-move-hint') 
                    actions.reset_actions()      
                    actions.click(pecas[i])
                    actions.perform()
                    if len(syshint) > 0:    
                        #time.sleep(1)                        
                        coord = Utils.get_coord(syshint[0].get_attribute("style"))
                        print(coord[0])
                        print(coord[1])
                        actions.reset_actions() 
                        actions.click(pecas[i])            
                        actions.move_to_element_with_offset(board,coord[0],coord[1])
                        actions.click()
                        actions.perform()                            
                        print("Jogada executada!")
                        break
                except WebDriverException as msg:
                    print(msg)
                    time.sleep(0.5)
            print("Aguardando oponente...")
            time.sleep(2)
        return

    @staticmethod
    def get_coord(lmh_style):
        style = str(lmh_style)
        a = style.find("transform")
        b = len(style)
        pixels = style[a+21:b-4]
        c = pixels.find("px")
        x = float(pixels[0:c])
        y = float(pixels[c+4:])
        return [x, y]
