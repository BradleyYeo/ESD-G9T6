from flask import Flask, render_template, redirect, abort, request

from models import db, InventoryModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/data/create', methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template('create.html')

    if request.method == "POST":
        id = request.form["product_id"]
        product_name = request.form["product_name"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        product = InventoryModel(id=id, product_name=product_name,
                                 quantity=quantity, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect("/data")


@app.route('/data')
def RetrieveDataList():
    inventory = InventoryModel.query.all()
    return render_template('datalist.html', inventory=inventory)


@app.route('/data/<int:id>')
def RetrieveSingleProduct(id):
    product = InventoryModel.query.filter_by(id=id).first()
    if product:
        return render_template('data.html', product=product)
    return f"Product with product_id ={id} Does not exist"


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


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    product = InventoryModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if product:
            db.session.delete(product)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


if __name__ == "__main__":
    app.run("localhost", port=5023, debug=True)
