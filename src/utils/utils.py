import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
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
        actions = ActionChains(driver)    
        board = driver.find_element(By.ID, "chessboard_boardarea")
        #style = str(board.get_attribute("style"))
        #a = style.find("height")
        #b = len(style)
        #size = float(style[a+8:b-3])
        #quad = size / 8
        #center = quad / 2
        while True:            
            pecas = driver.find_elements(By.CLASS_NAME, "chess_com_piece")
            print(len(pecas))
            for each in pecas:
                try:   
                    syshint = driver.find_elements(By.CLASS_NAME, 'legal-move-hint')   
                    print("antes1")
                    before1 = len(syshint)
                    print(before1)          
                    if before1 > 0:
                        driver.execute_script(""" 
                            var syshint = document.getElementsByClassName("legal-move-hint");
                            for (i = 0, len = syshint.length; i < len; i++) {
                                syshint[i].parentNode.removeChild(syshint[i]);
                            }
                        """)
                        time.sleep(1)
                    syshint = driver.find_elements(By.CLASS_NAME, 'legal-move-hint')   
                    print("antes2")
                    before = len(syshint)
                    print(before)
                    actions.reset_actions()      
                    actions.click(each)
                    actions.perform()  
                    time.sleep(2)
                    syshint = driver.find_elements(By.CLASS_NAME, 'legal-move-hint')   
                    print("meio3")
                    clicked = len(syshint)
                    print(clicked) 
                    actions.reset_actions()      
                    actions.click(each)
                    actions.perform()
                    if clicked > before:                                           
                        for cada in syshint:
                            style = str(cada.get_attribute("style"))
                            a = style.find("transform")
                            b = len(style)
                            pixels = style[a+21:b-4]
                            c = pixels.find("px")
                            x = float(pixels[0:c])
                            y = float(pixels[c+4:])
                            print(x)    
                            print(y)
                            print("tenta mover")
                            actions.reset_actions() 
                            actions.click(each)            
                            actions.move_to_element_with_offset(board,x,y)
                            actions.click()
                            actions.perform()                            
                            print("############Jogou##############")
                            time.sleep(0.3)
                            break
                        print("quebra o for")
                        break
                except WebDriverException as msg:
                    print(msg)
                    time.sleep(0.5)
            time.sleep(2)
        return
