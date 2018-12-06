from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        elem = driver.find_element_by_id('username')
        elem.clear()
        elem.send_keys(username)
        elem = driver.find_element_by_id('password')
        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        return
    
    @staticmethod
    def start_play(driver):
        while driver.current_url != "https://www.chess.com/play/computer":
            driver.get('https://www.chess.com/play/computer')
        try:
            elem = driver.find_element(By.CLASS_NAME, 'quick-challange')
            elem.click()
        except NoSuchElementException:
            print("Game Rolando")
        peca = driver.find_element(By.CLASS_NAME, 'chess_com_piece')
        x=5*60
        y=7*60
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(peca,x,y)
        actions.click() 
        actions.perform()  
        try:
            driver.execute_script(""" 
                var res = document.getElementsByClassName("legal-move-hint")[0].getAttribute("style"); 
                res = res.replace("pointer-events: none;", "")
                res = res.replace("width: 21px;", "width: 60px;")
                res = res.replace("height: 21px;", "height: 60px;")                
                element = document.createElement('div');            
                element.setAttribute("id", "highlight1");
                element.setAttribute("width", "60");
                element.setAttribute("height", "60");
                element.setAttribute("style", res)
                document.getElementById("chessboard_boardarea").appendChild(element);
            """)  
            hint = driver.find_element(By.ID, 'highlight1') 
            actions.reset_actions()
            actions.move_to_element(hint)
            actions.click() 
            actions.perform() 
            driver.execute_script("""               
                element = document.getElementById('highlight1');            
                document.getElementById("chessboard_boardarea").removeChild(element);
            """) 
        except WebDriverException:
            print(WebDriverException)
        #actions.move_by_offset(0,-120)        
        return