from urllib import request

from flask import Flask, render_template, redirect

from inventory.database import db, InventoryModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/data/create', methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("createpage.html")

    if request.method == "POST":
        id = request.form["id"]
        product_name = request.form["product_name"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        product = InventoryModel(id=id, product_name=product_name,
                                 quantity=quantity, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect("/data")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
