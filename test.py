from selenium import webdriver
from selenium.webdriver.common.by import By
import os , sys , time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
'''driver = webdriver.Firefox() 
link_site = "https://github.com/NickGkoutzas/autoClicker/blob/main/__carClicker__.py"    
driver.get(link_site)                        
raw = driver.find_element(By.CSS_SELECTOR , "#raw-url") 


action = ActionChains(driver)
action = action.context_click(raw).perform()

ActionChains.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
'''

i = 1
while(1):
    print("Hello  -> " + str(i))
    time.sleep(1)
    i += 1