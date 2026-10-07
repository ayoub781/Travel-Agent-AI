from scraping.meteo import scrape_meteo_historique,scrape_meteo_actuelle
from scraping.vols import scrape_vols
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
   
from guardrails import input_guardrail, output_guardrail
load_dotenv()
api_key=os.getenv("api_key")

#etape 1 car je ne sais pas ke faire de tete, on passe par une quesiton predefini, ensuite par le user input via le terminal, ensuite la on passe a la classe et ensuite on construire lagent. on passe don dun chatbot a un agent decisonnel.
class TravelAgent:
    def __init__(self):
        self.client=OpenAI(api_key=api_key)
        self.tool=[{
            "type":"function",
            "function":{
                "name":"scrape_meteo_historique",
                "description":"""Utilise cette fonction pour obtenir la météo historique d'une ville 
                                pour un mois spécifique. Appelle cette fonction quand l'utilisateur mentionne un mois 
                                précis (janvier, juin, décembre...) ou veut planifier un voyage futur.
                                Retourne la température max et min historiques pour ce mois.""",
                "parameters":{
                    "type": "object",
                    "properties":{
                        "country":{
                            "type":"string",
                            "description":"Pays en ANGLAIS et en minuscules (ex: japan, france, thailand)"
                        },
                        "city":{
                            "type":"string",
                            "description":"Ville d'où provient la météo"
                        },
                        "month":{
                            "type":"string",
                            "description":"Mois en FRANÇAIS et en minuscules (ex: janvier, fevrier, juin, aout, decembre)"
                        }


                    },
                    "required":["country","city","month"]
                }
            }

        },
        {"type":"function",
            "function":{
                "name":"scrape_meteo_actuelle",
                "description":"Fonction qui scrape les données meteorologique d'aujourdhui",
                "parameters":{
                    "type": "object",
                    "properties":{
                        "country":{
                            "type":"string",
                            "description":"Pays d'où provient la météo"
                        },
                        "city":{
                            "type":"string",
                            "description":"Ville d'où provient la météo"
                        }
                    },
                    "required":["country","city"]
                }
            }

        },
        {
    "type": "function",
    "function": {
        "name": "scrape_vols",
        "description": "Recherche les prix de vols aller-retour entre deux aéroports pour des dates spécifiques. Utilise cette fonction quand l'utilisateur veut connaître le prix d'un vol ou planifier un voyage avec des dates précises.",
        "parameters": {
            "type": "object",
            "properties": {
                "departure": {
                    "type": "string",
                    "description": "Code IATA de l'aéroport de départ en MAJUSCULES (ex: CDG pour Paris, NCE pour Nice, LHR pour Londres)"
                },
                "arrival": {
                    "type": "string",
                    "description": "Code IATA de l'aéroport d'arrivée en MAJUSCULES (ex: HND pour Tokyo Haneda, NRT pour Tokyo Narita, BKK pour Bangkok)"
                },
                "outbound_date": {
                    "type": "string",
                    "description": "Date du vol aller au format YYYY-MM-DD (ex: 2027-01-15)"
                },
                "return_date": {
                    "type": "string",
                    "description": "Date du vol retour au format YYYY-MM-DD (ex: 2027-02-15)"
                }
            },
            "required": ["departure", "arrival", "outbound_date", "return_date"]
        }
    }
}
        ]
        self.available_function={"scrape_meteo_historique":scrape_meteo_historique,
                            "scrape_meteo_actuelle":scrape_meteo_actuelle,
                            "scrape_vols":scrape_vols
        }
        self.message=[{"role":"system","content":
                       """
                    # Rôle & Objectif
                    Tu es un agent expert en météo et conseils de voyage. 
                    Tu aides les utilisateurs à choisir la meilleure destination ou période de voyage en te basant UNIQUEMENT sur des données météo réelles.

                    # Règles:
                    - Utilise TOUJOURS tes tools pour répondre, jamais tes connaissances générales
                    - Pays en ANGLAIS minuscules (japan, france, italy...)
                    - Villes en ANGLAIS minuscules (tokyo, paris, rome...)
                    - Mois en FRANÇAIS minuscules (janvier, juin, aout...)
                    - Pour la météo actuelle utilise scrape_meteo_actuelle
                    - Pour planifier un voyage utilise scrape_meteo_historique
                    - Précise TOUJOURS que les données historiques concernent les temperatures minimum et maximum de la période.

                    # Processus
                    Thought : Réfléchis d'abord, ai-je besoin d'un tool pour répondre ?
                    Action  : Si oui, appelle le ou les tools nécessaires simultanément si possible
                    Observation : Analyse le résultat obtenu
                    Thought : Ai-je encore besoin d'autres données ?
                    Action  : Si oui, appelle un autre tool. Sinon, formule ta réponse.
                    Answer  : Réponds en texte avec les données collectées
                       """}]
    def chat(self,user_input):

        
        input_ok,msg=input_guardrail(user_input)
        print(f"Guardrail result: {input_ok}, {msg}")
        if not input_ok:
            return msg,0
        self.message.append({"role":"user","content":user_input})
        counter=0
        max_iteration=10
        while True:
            if counter>=max_iteration:
                return("trop d'itération")
            response=self.client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=self.message,
                            tools=self.tool
                            )
            answer=response.choices[0].message.content
            if response.choices[0].message.tool_calls:
                self.message.append(response.choices[0].message)
                for tool_call in response.choices[0].message.tool_calls:
           
                    function_name=tool_call.function.name
                    args=tool_call.function.arguments
                    function_to_call=self.available_function[function_name]
                    result=function_to_call(**json.loads(args))
            
                    self.message.append({"role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":str(result)})

                
                counter+=1
            else:
                output_ok,msg=output_guardrail(answer)
                if not output_ok:
                    return msg,0
                else:
                    self.message.append(response.choices[0].message)#ici car An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'
                    return answer,counter


if __name__=="__main__":
    bot=TravelAgent()
    while True:
        user_input=input("entrez votre question: ")
   
        if user_input=="stop":
            break
        reponse, tours = bot.chat(user_input)
        print(f"Réponse : {reponse}")
        print(f"Tours : {tours}")
