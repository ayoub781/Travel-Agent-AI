
import requests

r=requests.post("http://127.0.0.1:5000/Chat",json={"message":"Je veux aller à Tokyo depuis Paris du 15 janvier au 15 février 2027, combien ça coûte et quel temps fera-t-il ?"},timeout=600)
print(r.text)
data=r.json()["response"]
tours=r.json()["tours"]
print(f"La réponse: {data}")
print(f"Tours: {tours}")

