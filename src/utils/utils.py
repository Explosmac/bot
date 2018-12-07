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
        while True:
            flag = False
            pecas = driver.find_elements(By.CLASS_NAME, "chess_com_piece")
            print(len(pecas))
            for each in pecas:
                try:
                    hint = driver.find_elements(By.CLASS_NAME, 'hlite')   
                    print("antes1")
                    print(len(hint))                  
                    if len(hint)>0: 
                        driver.execute_script(""" 
                            var hlite = document.getElementsByClassName("hlite");
                            for (i = 0, len = hlite.length; i < len; i++) {
                                hlite[i].parentNode.removeChild(hlite[i]);
                            }
                        """)
                    syshint = driver.find_elements(By.CLASS_NAME, 'legal-move-hint')   
                    print("antes2")
                    print(len(syshint))                  
                    if len(syshint)>0: 
                        driver.execute_script(""" 
                            var syshint = document.getElementsByClassName("legal-move-hint");
                            for (i = 0, len = syshint.length; i < len; i++) {
                                syshint[i].parentNode.removeChild(syshint[i]);
                            }
                        """)
                    hint = driver.find_elements(By.CLASS_NAME, 'hlite')   
                    print("meio1")
                    print(len(hint))
                    syshint = driver.find_elements(By.CLASS_NAME, 'legal-move-hint')   
                    print("meio2")
                    print(len(syshint))
                    actions.reset_actions()               
                    actions.move_to_element(each)
                    if flag:
                        actions.click(each)
                        actions.pause(0.1) 
                        actions.click(each)
                    else:
                        actions.click(each)
                        flag = True
                    actions.pause(0.1)
                    actions.perform()                     
                    driver.execute_script(""" 
                        var hint = document.getElementsByClassName("legal-move-hint");
                        var tot = "transform: translate(281.125px, 346.125px);".lenght;
                        for (i = 0, len = hint.length; i < len; i++) { 
                            var pontero = hint[i].getAttribute("style").toString();
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
                    print("depois")
                    print(len(hint))                   
                    for cada in hint:
                        print("tenta mover")
                        actions.reset_actions()
                        actions.click_and_hold(each)
                        actions.pause(0.1) 
                        actions.move_to_element(cada)
                        actions.pause(0.1) 
                        actions.release(cada) 
                        actions.pause(0.1) 
                        actions.perform()
                        time.sleep(0.1)
                        syshint = driver.find_elements(By.CLASS_NAME, 'legal-move-hint')
                        print(len(syshint))                        
                        if len(syshint) == 0:
                            flag = False
                            break
                    if len(hint) > 0:
                        break
                except WebDriverException as msg:
                    print(msg)
                    time.sleep(0.5)
            time.sleep(2)
        return
