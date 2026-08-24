from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def scrape_meteo_actuelle(country,city):
    country=country.lower()
    city=city.lower()
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.get(f"https://www.timeanddate.com/weather/{country}")
    time.sleep(2)
    table=driver.find_element(By.CSS_SELECTOR,"table.zebra.fw.tb-wt.zebra.va-m")
    lien=table.find_element(By.XPATH, f".//a[contains(@href, '/weather/{country}/{city}')]")
    city_name=lien.text
    #<a href="/weather/japan/asahikawa">Asahikawa</a>
    meteo=lien.find_element(By.XPATH,"./following::td[@class='rbi'][1]").text
    print(f"Meteo: {meteo}")
    print(f"City: {city_name}")
    driver.quit()
    return ({"Ville":city_name,"temperature_actuelle":meteo})

#print(scrape_meteo_actuelle("japan","Nagasaki")) 
def scrape_meteo_historique(country,city,month):
    country=country.lower()
    city=city.lower()
    month=month.lower()
    mois_mapping = {
    "janvier": "janvier",
    "fevrier": "février",
    "mars": "mars",
    "avril": "avril",
    "mai": "mai",
    "juin": "juin",
    "juillet": "juillet",
    "aout": "août",
    "septembre": "septembre",
    "octobre": "octobre",
    "novembre": "novembre",
    "decembre": "décembre"
    }
    month_converted={
    "janvier": "january",
    "février": "february",
    "mars": "march",
    "avril": "april",
    "mai": "may",
    "juin": "june",
    "juillet": "july",
    "août": "august",
    "septembre": "september",
    "octobre": "october",
    "novembre": "november",
    "décembre": "december"
    }
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.get(f"https://www.timeanddate.com/weather/{country}/{city}/climate")
    select_mois=Select(driver.find_element(By.ID,"tb-climate-select"))
    if month in month_converted:
        mois_exact=month
    elif month in mois_mapping:
        mois_exact=mois_mapping[month]
    else:
        driver.quit()
        return {"Erreur":  f"mois '{month}' non reconnu"}
    select_mois.select_by_visible_text(mois_exact)
    mois_en_anglais=month_converted[mois_exact]
    link=driver.find_element(By.CSS_SELECTOR,f"div.climate-month.climate-month--{mois_en_anglais}")
    paragraphes=link.find_elements(By.TAG_NAME,"p")
    for p in paragraphes:
        if "High Temp:" in p.text:
            High_Temp=p.text.replace("High Temp:","").strip()
          
        if "Low Temp:" in p.text:
            Low_Temp=p.text.replace("Low Temp:","").strip()
         
        
    
    driver.quit()
    return {
        "Month":mois_exact,
        "High_temp":High_Temp,
        "Low_temp": Low_Temp
    }



#restes a ajouter le try except ensuite tu ajouteras pour choisir la ville en fonction du mois etc. on va combiner ces 
#possibilite au sein de la meme fonction . MAIS DUCOUP FAUT AVOIR ACCES A TIME ZONE? ET SUROUT VU QUE CEST DU FUTR? BAH FAUT
#TRAITER DE CA dans le passé et le llm donnera une tendance sur a bonne periode ouo nan je crois bien .. 
