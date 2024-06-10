from bike import app, db
from flask import render_template, request, flash, url_for, redirect
from sqlalchemy import text


@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST']) #Database
def login_page():
    print("login was called")

    if request.method == 'POST':
        username = request.form.get('Username') # Holt dan von Browser zum Webserver
        password = request.form.get('Password')
        print("Logindaten: ")
        print(username)
        print(password)

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("not valid")
            flash(f"Username is not valid", category='warning')
            return render_template('login.html')

        if (password is None or
                isinstance(password, str) is False or
                len(password) < 3):
            print("something with password")
            flash(f"Password is not valid", category='warning')
            return render_template('login.html')

        query_stmt = f"select username from bikeusers where username = '{username}' and password = '{password}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))

        user = result.fetchall()
        if not user:
            flash(f"Try again", category='warning')
            return render_template('login.html')

        flash(f"'{user}', you are logged in ", category='success')
        resp = redirect('/bikes')
        resp.set_cookie('name', username)
        print("<-login(), go to bikes_pages")
        return resp
        #return redirect(url_for('bikes_page'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    print("register was called")

    if request.method == 'POST':
        username = request.form.get('Username')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        print('Register Data:')
        print(username)
        print(email)
        print(password1)
        print(password2)

        if(username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("username not valid")
            flash("Username not valid", category='danger')
            return render_template('register.html')

        if(email is None or
                isinstance(email, str) is False or
                len(email) < 3):
            print("email not valid")
            flash("Email not valid", category='danger')
            return render_template('register.html')

        if(password1 is None or
                isinstance(password1, str) is False or
                len(password1) < 3 or
                password1 != password2):
            print("Passwords not valid")
            flash("Password not valid", category='danger')
            return render_template('register.html')

        query_stmt = f"select * from bikeusers where username = '{username}'"
        print("query stmt: ", query_stmt)
        result = db.session.execute(text(query_stmt))
        item = result.fetchone()
        print("item: ", item)

        if item is not None:
            flash("Username already exists, try another one")
            print("Username already exists")
            return render_template('register.html')

        query_insert = f"insert into bikeusers (username, email_address, password) values ('{username}', '{email}', '{password1}')"
        print("query stmt: ", query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        flash("You have been registered successfully", category='success')
        resp = redirect('/bikes')
        resp.set_cookie('name', username)
        print("<-register_page(), go to bikes_page")
        return resp

        #return redirect(url_for('bikes_page'))

    return render_template('register.html')

@app.route('/bikes') #Database
def bikes_page():

    cookie = request.cookies.get('name')
    print("->bikes_page()", cookie)
    if not request.cookies.get('name'):
        print("<-bikes_page(), no cookie")
        return redirect(url_for('login_page'))

    query_stmt = f"select * from bikefeatures"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()

    print(itemsquery)
    print("<-bikes_page()= ", cookie)
    return render_template('bikes.html', items=itemsquery, cookie=cookie) # keyword=variable-> wird in bikes.html reingegeben

@app.route('/logout')
def logout():
    resp = redirect('/')
    resp.set_cookie('name', '', expires=0)
    return resp

@app.route('/bike_entry', methods=['GET', 'POST'])
def bike_entry():

    cookie = request.cookies.get('name')
    print("->bike_entry()", cookie)
    if not cookie:
        print("no cookie")
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        bikename = request.form.get('bikename')
        size = request.form.get('size')
        user = request.form.get('user')
        description = request.form.get('description')

        query_insert = f"insert into bikefeatures (bikename, size, user, description) values ('{bikename}', '{size}', '{user}', '{description}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        print("POST erfolgreich")
        resp = redirect('/bikes')
        resp.set_cookie('name', cookie)
        return resp

    return render_template('bike_entry.html', cookie=cookie)

@app.route('/bike_item/<int:item_id>', methods=['GET'])
def bike_item(item_id):
    print("->bike_item()")
    query_stmt = f"select * from bikefeatures where id={item_id}"

    result = db.session.execute(text(query_stmt))
    item = result.fetchone()
    print(query_stmt)
    if not item:
        print("item not existing")
        # error handling ....

    cookie = request.cookies.get('name')

    return render_template('bike_item.html', items=item, cookie=cookie)
