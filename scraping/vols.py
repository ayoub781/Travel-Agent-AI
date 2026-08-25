import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_flights")
def scrape_vols(departure, arrival, outbound_date, return_date):
    url="https://www.searchapi.io/api/v1/search"
    print(f" Fonction scrape_vols appelé : From {departure} to {arrival}") # Je mets cela afin que l'on sache si l'agent a bien répondu à l'aide de la focniton.
   
    params = {
        "engine": "google_flights",
        "departure_id": departure,
        "arrival_id": arrival,
        "outbound_date": outbound_date,
        "return_date": return_date,  
        "api_key": api_key
    }
    

    response = requests.get(url, params=params)
    data = response.json()
    #print(data.keys())
    #print(f"voici la data : {data['best_flights'][0]}")
    
    if "best_flights" in data: #On met ces 2 conditions car avec seulement "best_flights" j'obtenait une erreur indiquant qu'il n'existe pas de best_flights pour le billet retour. Nous avons donc ajouté le fallback other_flights
        vols = data["best_flights"]
        source = "best_flights"
    elif "other_flights" in data:
        vols = data["other_flights"]
        source = "other_flights"
    if not vols:   
        return {"erreur": "Aucun vol trouvé"}
   
    best_flights= {
            "prix" : vols[0]["price"],
            "duree" : vols[0]["total_duration"],
            "compagnie" : vols[0]["flights"][0]["airline"],
            "source": source
        }
    departure_token=vols[0]["departure_token"]
    #Je mets volontairement vols[0] et non pas les 3 departures token (associés aux 3 best_flights) car l'api nous permet uniquement 100 appels gratuits par mois, mais je laisse tout de meme la boucle sur les 3 best_flights au cas où à l'avenir je voudrais rajouter les 3 differents departures_token.
    
    params2 = params.copy()
    params2["departure_token"]=departure_token
    data_return_flight=requests.get(url,params=params2).json()
    #print(f"voici le return final: {data_return_flight}")
    vols_retour=data_return_flight.get("best_flights",data_return_flight.get("other_flights",[]))
    booking_token = vols_retour[0]["booking_token"]
    params3 = params.copy()
    params3["booking_token"]=booking_token
    data3 = requests.get(url, params=params3).json()
    #print(f"voici le lien de reservation: {data3}")
    lien_google_flights = data3["search_metadata"]["request_url"]
 
   
    return {
    "trajet": f"from {departure} to {arrival}",
    "outbound_date": outbound_date,
    "return_date": return_date,
    "prix_minimum": data["price_insights"]["lowest_price"],
    "meilleurs_vols": best_flights,
    "lien_vol":lien_google_flights
    }


