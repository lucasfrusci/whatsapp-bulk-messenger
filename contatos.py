from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ScrollOrigin
import time


def buscar_contatos(driver, tbNumeros, send):
    if driver == None:
        send("Erro: Nenhum grupo encontrado!", "red")
        return
        
    
    #elements = driver.find_elements(By.CLASS_NAME, 'x1iyjqo2.x6ikm8r.x10wlt62.x1n2onr6.xlyipyv.xuxw1ft.x1rg5ohu._ao3e')
    #elements = driver.find_elements(By.XPATH, "//*[@title][starts-with(@title, '+55')]")
    elements = driver.find_elements(By.XPATH, "//span//div[contains(@class, 'x1n2onr6 x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf')]//*[@class][starts-with(@class, '_ao3e')]")
    elements2 = driver.find_elements(By.XPATH, "//span//div[contains(@class, 'x1n2onr6 x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf')]//*[@title][starts-with(@title, '+')]")

    for element in elements2:
        contact = element.text.strip()
        send("Numero adicionado:" + contact, "white")
        if contact:
            contact = contact.replace(" ", "")
            contact = contact.replace("-", "")
            tbNumeros.insert("end", contact + "\n")
            tbNumeros.see("end")
            
    for element in elements:
        contact = element.text.strip()
        send("Numero adicionado:" + contact, "white")
        if contact:
            contact = contact.replace(" ", "")
            contact = contact.replace("-", "")
            tbNumeros.insert("end", contact + "\n")
            tbNumeros.see("end")
    
        
def scrool(driver, tbNumeros, send):
    #scroll = driver.find_elements(By.XPATH, 'x1n2onr6.x1n2onr6.xyw6214.x78zum5.x1r8uery.x1iyjqo2.xdt5ytf.x6ikm8r.x1odjw0f.x1hc1fzr.x1tkvqr7')
    scroll = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div/div[2]')
    #driver.execute_script("arguments[0].scrollBy(0, 1296);", scroll[0])
    
    
    if scroll:
        pass
    else:
        send("Abra lista de numeros do GRUPO!", "yellow")

    while scroll is not None:
        scroll_position = driver.execute_script("return arguments[0].scrollTop;", scroll[0])
        scroll_height = driver.execute_script("return arguments[0].scrollHeight;", scroll[0])
        visible_height = driver.execute_script("return arguments[0].clientHeight;", scroll[0])
        time.sleep(0.2)
        buscar_contatos(driver, tbNumeros, send)
        if scroll_position + visible_height >= scroll_height - 50:
            scroll = None
            return
        else:
            driver.execute_script("arguments[0].scrollBy(0, 1296);", scroll[0])

#contacts = get_group_contacts
#print(f"Contatos encontrados ({len(contacts)}):")
#for contact in contacts:
#    print(contact)