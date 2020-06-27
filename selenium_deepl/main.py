from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import os, time
import pyperclip as clip


driver = None
src = None
dst = None


def init():
    global driver, src, dst
    # open the deepl
    driver = webdriver.Chrome()
    driver.get("https://www.deepl.com/translator")
    elements = driver.find_elements_by_xpath("//textarea")
    src = elements[0]
    dst = elements[1]
    # select english
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[3]/div[1]/div/button/div").click()
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[3]/div[1]/div/div/button[3]").click()


def translate(english):
    global src, dst
    clip.copy(english)
    src.send_keys(Keys.CONTROL, "a")
    src.send_keys(Keys.CONTROL, Keys.DELETE)
    src.send_keys(Keys.CONTROL, "v")
    clip.copy("")
    while clip.paste() == "":
        time.sleep(1)
        try:
            dst.send_keys(Keys.CONTROL, "a")
            dst.send_keys(Keys.CONTROL, "x")
        except:
            pass
    return clip.paste()


def output(result):
    with open(os.path.dirname(__file__) + "/out.txt", "a", encoding="utf-8") as f:
        f.write(result)


if __name__ == "__main__":
    init()
    base_text = ""
    with open(os.path.dirname(__file__) + "/src.txt", "r", encoding="utf-8") as f:
        base_text = f.read()
    begin, end = 0, 0
    while True:
        begin = end
        end = base_text.rfind(".", begin, begin + 4980) + 1
        if end == 0:
            break
        print("translation bytes from %d to %d" % (begin, end))
        output(translate(base_text[begin: end]))
    driver.quit()
    print("done")