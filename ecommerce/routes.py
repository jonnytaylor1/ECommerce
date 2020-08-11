from flask import render_template, url_for, flash, redirect, session, request
from ecommerce import app, db
from ecommerce.models import User, TShirt
from flask_login import login_user, current_user, logout_user
from collections import Counter


app.secret_key = "hello"

# Renders the home page and passes loads the T-shirts info
@app.route("/")
def home():
    tshirts = TShirt.query.all()
    return render_template("index.html", tshirts = tshirts)

# Renders the login page (inc redirects depending on user login status)
@app.route("/login", methods=[ "GET", "POST"])
def login():
    if 'user' not in session:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            found_user = User.query.filter(User.email == email).first()
            if found_user and found_user.password == password:
                session['user'] = found_user.id
                flash("Login successful. You are now able to add items to your basket")
                return redirect(url_for("home"))
            else:
                flash('Login unsuccessful. Please check email and password!')
        return render_template("login.html")
    else:
        return redirect(url_for("home"))

# Renders the signup page (inc redirects depending on user signup status)
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if 'user' not in session:

        if request.method == 'POST':
            firstName = request.form["firstName"]
            surname = request.form["surname"]       
            email = request.form["email"]
            password = request.form["password"]

            duplicateEmail = User.query.filter(User.email == email).first()
            if duplicateEmail:
                flash("The email entered has already been registered, please login or use a different email")
            else:
                newUser = User(firstName, surname, email, password)
                db.session.add(newUser)
                db.session.commit()
                flash('Successful sign up. Please login.', "info")
                return redirect(url_for("login"))
        
        return render_template("signup.html")
    else:
        return redirect(url_for("home"))

# Renders the individual T-shirt page where the user can add the Tshirt to the basket, if logged in
@app.route("/tshirt/<tshirtId>", methods=["POST", "GET"])
def extraDetails(tshirtId):
    try:
        tshirtDetails = TShirt.query.filter(TShirt.id == tshirtId).first()
        if tshirtDetails is not None:
            fineDetails = tshirtDetails.tshirt_details['details']
            fineDetailsList = fineDetails.split(",")
            if request.method == 'POST':
                if 'user' in session:
                    if request.form.get('basket') == 'Add to Basket':
                        if 'basketId' not in session:
                            session['basketId'] = []

                        session['basketId'].append(tshirtDetails.id)
                        flash('{} has been added to the basket'.format(tshirtDetails.tshirt_details['product']), "info")
                    elif request.form.get('wishlist') == 'wishlist':
                        # Please ignore the code between lines 78-81
                        print('this was for if I did a wishlist')
                        # user id is in the session ie session['user']
                        # tshirt id is tshirtDetails.id
                        # you need to add to the join table
                else:
                    flash("You can only add to the basket once you have signed in", "info")
                    return redirect(url_for("login"))
            return render_template("extraDetails.html", tshirtDetails=tshirtDetails, fineDetails = fineDetailsList)
        else:
            return render_template("404.html")
    except Exception as e:
        return render_template("500.html")

# Currently not functional
@app.route("/wishlist")
def wishlist():
    return render_template("wishlist.html")

# Renders the basket page where the user can increase/decrease/delete
# the current items in their basket. The user can also proceed to checkout.
# Need to add redirect if the user is not logged in
@app.route("/basket", methods=["POST", "GET"])
def basket():
    
    id = 0
    basketIdAndFrequency = []
    tshirtBasket = []
    basketTotal = 0
    sortedBasket = []
    newSession = []
    quantity = 0
    if request.method == 'POST':

        if request.form.get("change") == 'Increase Quantity':
            id = request.form['productId']
            session['basketId'].append(int(id))

        elif request.form.get("change") == 'Decrease Quantity':
            id = request.form['productId']
            sessionData = list(session['basketId'])
            sessionData.remove(int(id))
            session['basketId'] = sessionData


        elif request.form.get("change") == 'Remove Item':
            id = request.form['productId']
            newSession = [value for value in session['basketId'] if value != int(id)]
            session['basketId'] = newSession
            if session['basketId'] == []:
                flash("Empty Basket", "info")

        elif request.form.get("change") == 'Empty Basket':
            session.pop('basketId')

        elif request.form.get('productId'):
            id = request.form.get('productId')
            newSession = [value for value in session['basketId'] if value != int(id)]
            session['basketId'] = newSession
            quantity = request.form['quantity']
            for i in range(int(quantity)):
                session['basketId'].append(int(id))


    try:
        if session['basketId'] == []:
            flash("Empty Basket", "info")
        sortedBasket = sorted(session['basketId'])
    
        def group_list(lst): 
            return list(zip(Counter(lst).keys(), Counter(lst).values()))

        basketIdAndFrequency = group_list(sortedBasket)
        tshirtIds = [i[0] for i in basketIdAndFrequency]
        tshirtQuantity = [i[1] for i in basketIdAndFrequency]
        basketTotal = 0 
        tshirtBasket = []
        for i in range(len(tshirtIds)):
            tshirtDetails = TShirt.query.filter(TShirt.id == tshirtIds[i]).first()
            tshirtBasket.append(
                {"id": tshirtIds[i],
                "imageUrl": tshirtDetails.tshirt_details['imageUrl'],
                "quantity": tshirtQuantity[i],
                "product": tshirtDetails.tshirt_details['product'],
                "price": tshirtDetails.tshirt_details['price'],
                "product_total": str(format(int(tshirtQuantity[i]) * float(tshirtDetails.tshirt_details['price']), '.2f'))
                }
            )
            basketTotal += int(tshirtQuantity[i]) * float(tshirtDetails.tshirt_details['price'])  
        
        basketTotal = str(format(basketTotal, '.2f'))
    
    except KeyError:
        flash("Empty Basket", "info")

    if request.method == 'POST':
        if request.form.get('checkout') == 'checkout':
            session['amountPayable'] = basketTotal
            return redirect(url_for('checkout'))

    return render_template("basket.html", basketIdAndFrequency=basketIdAndFrequency, tshirtBasket=tshirtBasket, basketTotal=basketTotal, sortedBasket=sortedBasket, id=id, newSession = newSession, quantity=quantity)

# Checkout payment page (not linked to payment system)
@app.route("/checkout", methods=["POST", "GET"])
def checkout():
    if request.method == 'POST':
        session.pop('basketId')
        flash("Your payment has been made. Thank you for shopping with us! :)", "info")
        return redirect(url_for('home'))    

    else:
        amountPayable = session['amountPayable']
        return render_template("checkout.html", amountPayable=amountPayable)


# User redirected to home page and their session is removed
@app.route("/logout")
def logout():
    session.pop('user')

    try:
        session.pop('basketId')
    except KeyError:
        print('No items in basket')

    flash("You have been logged out!", "info")
    return redirect(url_for("home"))


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")
