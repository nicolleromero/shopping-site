"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, request, session
import jinja2

import melons
import customers

app = Flask(__name__)


# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()

    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)

    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    cart = session.get('cart', {})
    total = session.get('total', 0)

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    return render_template("cart.html",
                           cart=cart,
                           melon_types=melons.melon_types,
                           total=total)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""
    # session['cart'] is a dict
    # session['cart'][melon_id]
    # if 'cart' not in session:
    # session['cart'] = {}

    melon_list = melons.get_all()

    cart = session.get('cart', {})
    cart[melon_id] = cart.get(melon_id, 0) + 1
    session['cart'] = cart

    total = 0
    for item in cart:
        total += (melons.melon_types[item].price * cart[item])

    melon_name = melons.melon_types[item].common_name
    flash(f"You've successfully added one {melon_name} to your cart.")
    session['total'] = total

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    email = request.args.get("email")
    password = request.args.get("password")

    return render_template("login.html",
                           email=email,
                           password=password)


@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    customers_list = customers.read_customers_from_file("customers.txt")

    if email in customers_list.keys():
        customer = customers.get_by_email(email)

        if customer.password == password:
            flash("Login successful!")
            session['logged_in_customer_email'] = email
            session.get('logged_in_customer_email')
            return redirect("/melons")

        else:
            flash("The password you entered is incorrect.")
            return redirect("/login",
                            logged_in_customer_email=logged_in_customer_email)
    else:
        flash("The email you entered does not match our records.")
        return redirect("/login",
                        logged_in_customer_email=logged_in_customer_email)

    # error = None

    # if request.method == 'POST':
    #     if valid_login(request.form['email'],
    #                    request.form['password']):
    #         return log_the_user_in(request.form['email'])
    #     else:
    #         error = 'Invalid email/password'
    # # the code below is executed if the request method
    # # was GET or the credentials were invalid
    # return render_template('login.html', error=error)

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist


@app.route("/logout")
def process_logout():
    """Log user into site.

    Delete the user's login credentials from the session.
    """
    del session['logged_in_customer_email']

    flash("You are now logged out.")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
