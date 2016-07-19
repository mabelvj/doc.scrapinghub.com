from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import *

polipo_proxy = "localhost:8123"

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': polipo_proxy,
    'ftpProxy' : polipo_proxy,
    'sslProxy' : polipo_proxy,
    'noProxy'  : ''
})

driver = webdriver.Firefox(proxy=proxy)
driver.get("http://scrapinghub.com")
assert "Scrapinghub" in driver.title
elem = driver.find_element_by_class_name("portia")
actions = ActionChains(driver)
actions.click(on_element=elem)
actions.perform()
print "Clicked on Portia!"
driver.close()
