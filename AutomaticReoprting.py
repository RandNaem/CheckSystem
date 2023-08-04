# driver configuration
from behave import given, then, when
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import random
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.microsoft import EdgeChromiumDriverManager
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--lang=eng')
chrome_services = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=chrome_services, options=chrome_options)
driver.maximize_window()
# automation task
driver.get("http://127.0.0.1:8000/admin/")
driver.find_element(By.CSS_SELECTOR, "#id_username").send_keys("RandTopDev")
driver.find_element(By.CSS_SELECTOR, "#id_password").send_keys("randyouarethebest")
driver.find_element(By.XPATH, "//input[@value='Log in']").click()
driver.find_element(By.XPATH, "//a[normalize-space()='In outs']").click()
driver.find_element(By.CLASS_NAME, "export_link").click()
formats_dropdown = Select(driver.find_element(By.CSS_SELECTOR, "#id_file_format"))
formats_dropdown.select_by_visible_text("xlsx")
driver.find_element(By.CLASS_NAME, "default").click()
