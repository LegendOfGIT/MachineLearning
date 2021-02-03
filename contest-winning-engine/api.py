import flask
import model
import mysql.connector
import numpy as np

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def get_percentage(current_amount, total_amount):
  if total_amount == 0:
    return 100

  return (current_amount * 100) / total_amount

def getDatabase():
    db = mysql.connector.connect(
      host="mysql",
      user="root",
      password="",
      database="contest-winning"
    )

    return db

def createTablesWhenNecessary():
    db = getDatabase()
    cursor = db.cursor()
    cursor.execute("SHOW TABLES LIKE 'participations'")
    if not cursor.fetchone():
        cursor.execute('CREATE TABLE participations (id INT AUTO_INCREMENT PRIMARY KEY, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, has_won tinyint DEFAULT 0)')
        db.commit()

def addParticipationToTable(has_won):
    db = getDatabase()
    cursor = db.cursor()
    cursor.execute("INSERT INTO participations(has_won) VALUES(" + str(has_won) + ")")
    db.commit()

def get_current_prices_give_out_tendency_in_percent():
    db = getDatabase()
    cursor = db.cursor()
    cursor.execute("SELECT has_won FROM participations ORDER BY id DESC LIMIT 35")

    last_give_outs = []
    for has_won in cursor.fetchall():
         last_give_outs.append(has_won[0])

    if (0 == len(last_give_outs)) :
        return 0

    return get_percentage(np.count_nonzero(last_give_outs), len(last_give_outs))

@app.route('/', methods=['GET'])
def home():
    createTablesWhenNecessary()

    if flask.request.args.get('pricesLeftInPercent') == None:
        return flask.jsonify(error = 'PARAMETER_NOT_GIVEN', parameter = 'pricesLeftInPercent')

    if flask.request.args.get('timePassedInPercent') == None:
        return flask.jsonify(error = 'PARAMETER_NOT_GIVEN', parameter = 'timePassedInPercent')

    prices_left_in_percent = float(flask.request.args.get('pricesLeftInPercent'))
    time_passed_in_percent = float(flask.request.args.get('timePassedInPercent'))

    prices_give_out_tendency_in_percent = get_current_prices_give_out_tendency_in_percent()

    give_out_price = model.run_model(
        time_passed_in_percent,
        prices_left_in_percent,
        prices_give_out_tendency_in_percent
    )
    addParticipationToTable(1 if give_out_price else 0)

    return flask.jsonify(
        error = '',
        give_out_price = give_out_price,
        prices_give_out_tendency_in_percent = prices_give_out_tendency_in_percent,
        prices_left_in_percent = prices_left_in_percent,
        time_passed_in_percent = time_passed_in_percent
    )

app.run(host='0.0.0.0')
