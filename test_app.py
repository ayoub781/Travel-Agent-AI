
import requests

r=requests.post("http://127.0.0.1:5000/Chat",json={"message":"Jje veux aller a hanoi au vietnam du 15 janvier 2027 au 30 janvier 2027 en partant de paris, esque la meteo y sera bonne et trouves moi le billet le moins cher"})
print(r.text)
data=r.json()["response"]
tours=r.json()["tours"]
print(f"La réponse: {data}")
print(f"Tours: {tours}")

