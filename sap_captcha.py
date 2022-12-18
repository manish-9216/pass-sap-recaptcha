# Solve reCaptcha V2 with Selenium Python Using 2captcha
from selenium import webdriver
import requests, time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import os
import random
import urllib


audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"

user_name = "S0020962433"
pwdd = 'Qwerty1!!'



page_url ="https://accounts.sap.com/saml2/idp/sso?SAMLRequest=fZLLbsIwEEV%2FxfLeiRMgCRYJokWoSH1EJe2im8o4TrGU2KnH6ePvGwJUdFG2M3funTn2bP7V1OhDWlBGpzjwKEZSC1Mq%2FZbip2JFEjzPZsCbOmzZonM7%2FSjfOwkO9YMa2KGT4s5qZjgoYJo3EpgTbLO4u2WhR1lrjTPC1Bgt%2B0GluRvCds61wHyfC2E67cAD3nrCNP7g6auy9QEMRitjhRyiU%2BxsJzFaL1P8ug2qWMRJQgStxmQcTyiZ8igiAR%2BFYjqKx1WQ9FKATq41OK5dikMahoRGZEQLGrEgZJPYo%2BH0BaP8uOOV0ofbLx20PYiA3RRFTvKHTYHR84lhL8BHYmxIt%2BeoLhtzAGn3dHB2otM2wGsJpWxM4kEnhASouHDGwh7WzD9P%2Bn2p%2B956vcxNrcQ3WtS1%2Bby2kjt5Itgzbbj7f5nAC4aKKkk1SFmnoZVCVUqW2M%2BOsX%2B%2FRPYD&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=X1qusd7tGp5sgApR1tsbnmC0im7L%2B6tfw2bue%2FF2r%2B%2BdreQLsNsq%2BW40DEajncSvcP8sq3rcCeBPQhX%2BghiI9A58Sa99jahszHeZEOHTkBa05XuOj8SqT9TheUb8RRpGKX6zb9y5DmT2xLtHfGulu83itA5zogHZcOCGprxi24I%3D"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()


def reCaptchaSolver():
    # here hitting url of login page 
    driver.get(page_url)
    time.sleep(10)    
    # sending credential in login page 
    driver.find_element_by_xpath("//input[@id='j_username']").send_keys(user_name)
    driver.find_element_by_xpath("//div[@class='fn-button__text']").click()
    time.sleep(15)

    switch_to_iframe(driver)
   
    audioBtnFound = checking_captcha_frame(driver)
    
    if audioBtnFound == True:
        set_audio_text(driver) 
    else:
        driver.switch_to.default_content()
        submit_button(driver)

        return True
    


def delay():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    result = text.text
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result

def checking_captcha_frame(driver):
    audioBtnFound = False
    
    try:
        audioBtn = driver.find_element_by_id("recaptcha-audio-button")
        audioBtn.click()
        audioBtnFound = True

    except Exception as e:
        pass
    
    return audioBtnFound


def switch_to_iframe(driver):
    iframe = driver.find_element_by_xpath("//iframe[@title='recaptcha challenge expires in two minutes']")
    driver.switch_to.frame(iframe)
    
    return True


def submit_button(driver):
    driver.find_element_by_xpath("//input[@id='password']").send_keys(pwdd)
    try:
        button = driver.find_element_by_xpath("//button[@class='uid-login-as__submit-button test-button ds-button ds-button--primary']").click()
    except: 
        button = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/form/div/div[2]/button").click()
    print("Login Button =>", button)
    
    return True

def set_audio_text(driver):
    try:
        while True:
            # get the mp3 audio file
            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print("[INFO] Audio src: %s" % src)

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech To Text Conversion
            key = audioToText(os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key: %s" % key)
            time.sleep(2)

            # switching iframe
            switch_to_iframe(driver)
            time.sleep(2)
            
            inputField = driver.find_element_by_id("audio-response")
            inputField.send_keys(key)
            delay()

            inputField.send_keys(Keys.ENTER)
            delay()
            driver.switch_to.default_content()
            time.sleep(2)
            
            button = submit_button(driver)
            print("Login Button =>", button)
            
            return True
            
    except Exception as e:
        print(e)
        sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
        

if __name__ == '__main__':
    reCaptchaSolver()
