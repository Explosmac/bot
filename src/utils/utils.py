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
        driver = webdriver.Firefox()
        driver.get('https://www.chess.com/login')
        return driver

    @staticmethod
    def login(driver, username, password):
        elem = driver.find_element_by_id('username')
        elem.clear()
        elem.send_keys(username)
        elem = driver.find_element_by_id('password')
        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        return

    @staticmethod
    def play_game(driver):
        while driver.current_url != "https://www.chess.com/play/computer":
            driver.get('https://www.chess.com/play/computer')
        while True:
            pecas = driver.find_elements(By.CLASS_NAME, "chess_com_piece")
            print(len(pecas))
            for each in pecas:
                try:         
                    hint = driver.find_elements(By.CLASS_NAME, 'hlite')                     
                    if len(hint)>0: 
                        driver.execute_script(""" 
                            var board = document.getElementsByClassName("hlite");
                            for (i = 0, len = board.length; i < len; i++) {
                                document.getElementById("chessboard_boardarea").removeChild(board[i]);
                            }
                        """)      
                    actions = ActionChains(driver)
                    actions.move_to_element(each)
                    actions.click() 
                    actions.perform() 
                    driver.execute_script(""" 
                        var board = document.getElementsByClassName("legal-move-hint");
                        var tot = "transform: translate(281.125px, 346.125px);".lenght;
                        for (i = 0, len = board.length; i < len; i++) { 
                            var pontero = board[i].getAttribute("style").toString();
                            //var pos = pontero.search("trasform");
                            var nsty = "position: absolute; margin: 0px; padding: 0px; display: block; overflow: hidden; opacity: 1; width: 65px; height: 65px; z-index: 12;" + pontero.slice(-tot);
                            //pontero = pontero.replace("pointer-events: none;", "display: block;");
                            element = document.createElement('div');
                            element.setAttribute("class", "hlite");
                            element.setAttribute("width", "30");
                            element.setAttribute("height", "30");
                            element.setAttribute("style", nsty)
                            document.getElementById("chessboard_boardarea").appendChild(element);
                        }
                    """)  
                    hint = driver.find_elements(By.CLASS_NAME, 'hlite')                     
                    for cada in hint:
                        actions.reset_actions() 
                        actions.move_to_element(each)
                        actions.click_and_hold()
                        actions.move_to_element(cada)
                        actions.release() 
                        actions.perform()
                except WebDriverException as msg:
                    print(msg)
                pecas = driver.find_elements(By.CLASS_NAME, "chess_com_piece")
            time.sleep(1)
        #actions.move_by_offset(0,-120)
        
        return