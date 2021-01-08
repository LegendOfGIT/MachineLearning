import flask
import model

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    if flask.request.args.get('pricesLeftInPercent') == None:
        return flask.jsonify(error = 'PARAMETER_NOT_GIVEN', parameter = 'pricesLeftInPercent')

    if flask.request.args.get('timePassedInPercent') == None:
        return flask.jsonify(error = 'PARAMETER_NOT_GIVEN', parameter = 'timePassedInPercent')

    if flask.request.args.get('pricesGiveOutTendencyInPercent') == None:
        return flask.jsonify(error = 'PARAMETER_NOT_GIVEN', parameter = 'pricesGiveOutTendencyInPercent')

    prices_give_out_tendency_in_percent = float(flask.request.args.get('pricesGiveOutTendencyInPercent'))
    prices_left_in_percent = float(flask.request.args.get('pricesLeftInPercent'))
    time_passed_in_percent = float(flask.request.args.get('timePassedInPercent'))

    return flask.jsonify(
        error = '',
        give_out_price = model.run_model(
            time_passed_in_percent,
            prices_left_in_percent,
            prices_give_out_tendency_in_percent
        ),
        prices_give_out_tendency_in_percent = prices_give_out_tendency_in_percent,
        prices_left_in_percent = prices_left_in_percent,
        time_passed_in_percent = time_passed_in_percent
    )

app.run(host='0.0.0.0')
