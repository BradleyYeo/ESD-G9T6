from flask import Flask, render_template, redirect, abort, request, jsonify

from models import db, InventoryModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/inventory/all')
def get_all():
    inventory = InventoryModel.query.all()
    if len(inventory):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [item.json() for item in inventory]
                },
                "message": "all items retrieved"
            }
        )
    return jsonify(
        {
            "code": 500,
            "data": {},
            "message": "There is no inventory recorded in the database"
        }
    )
    # return render_template('datalist.html', inventory=inventory)


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    product = InventoryModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if product:
            db.session.delete(product)
            db.session.commit()
            name = request.form['product_name']
            quantity = request.form['quantity']
            price = request.form['price']
            product = InventoryModel(id=id, product_name=name, quantity=quantity, price=price)
            db.session.add(product)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Product with product_id = {id} Does not exist"

    return render_template('update.html', product=product)


if __name__ == "__main__":
    app.run("localhost", port=5023, debug=True)
