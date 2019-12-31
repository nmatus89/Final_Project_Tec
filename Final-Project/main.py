from flask import Flask, render_template, redirect, jsonify
from bson.json_util import loads, dumps
#Local imports
import Smart_bet_v1

app = Flask(__name__)

@app.route("/")
def home():
    #Get mars dict
    ##data_webpage = charts.consult_snap_db()
    ##data_webpage = dumps(data_webpage)
    #Return template and data
    #return render_template("index.html", data_app=data_webpage)
    
    #Llama las funciones que hacen el scrap, los cálculos y generan los diccionarios
    laliga=Smart_bet_v1.laliga_top_picks()
    bundesliga=Smart_bet_v1.bundesliga_top_picks()
    premier=Smart_bet_v1.premier_top_picks()

    return render_template("index.html", picks_laliga=laliga, picks_bundesliga=bundesliga, picks_premier=premier)


if __name__ == "__main__":
    app.run(debug=True)