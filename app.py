from flask import Flask,jsonify,request
from chatbot import TravelAgent
app=Flask(__name__)
bot=TravelAgent()
@app.route("/Chat", methods=["POST"])
def ChatAi():
    user_input=request.json["message"]
    response,tours=bot.chat(user_input)
    return jsonify({"response":response,
                    "tours": tours})
   
    
if __name__=="__main__":
    app.run(debug=True,use_reloader=False)
