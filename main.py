from flask import Flask
from blueprint.api_pharmacy import bp_pharmacy_api
from blueprint.api_transaction import bp_transaction_api
from blueprint.api_mask import bp_mask_api


app = Flask(__name__)
app.register_blueprint(bp_pharmacy_api)
app.register_blueprint(bp_transaction_api)
app.register_blueprint(bp_mask_api)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, debug=True)
    # create_tables()
