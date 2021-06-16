from flask import Flask, request
from hashlib import sha256
import random
import string


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return """<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>DROM Chain</title>
</head>
<body>
    <h1 style="text-align: center;margin-top: 10%">DROM Chain</h1>
    <form action="/profile" style="text-align: center;" method="post">
        <input type="text" placeholder="Login" required minlength="10" required name="login">
        <br>
        <br>
        <input type="text" placeholder="Password" required minlength="20" name="password">
        <br>
        <br>
        <input type="text" placeholder="Address" required name="address">
        <br>
        <br>
        <input type="submit" value="Sign in">
        <a href="/create_wallet"><p>Create wallet</p></a>
    </form>
</body>
</html>"""

@app.route('/create_wallet', methods=["GET"])
def creation():
    return """<!DOCTYPE HTML>
    <html>
    <head>
    <meta charset="utf-8">
    <title>DROM Chain</title>
    </head>
    <body>
        <h1 style="text-align: center;margin-top: 10%">Create DROM Wallet</h1>
        <form action="/wallet_created" style="text-align: center;" method="post">
            <input type="text" placeholder="Login" minlength="10" required name="login">
            <br>
            <br>
            <input type="text" required minlength="20" placeholder="Password" name="password">
            <br>
            <br>
            <input type="submit" value="Create">
            <a href="/"><p>Sign in</p></a>
        </form>
    </body>
    </html>"""


@app.route('/wallet_created', methods=["GET", "POST"])
def creation_info():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        address = sha256(str(password+login).encode('utf-8')).hexdigest()
        try:
            f = open(address + ".txt", "r")
            test = float(f.read())
            return """<body style="text-align:center;">
                                <h1>Sorry!</h1>""" + "<br><br><p>Address with this password/login already exist!</p>"+ """
                                <a href="/create_wallet"><p>Create another wallet</p></a>"""
        except Exception:
            f = open(address + ".txt", "w")
            f.write("0.0")
            f = open(address + ".txt", "r")
            blnc = float(f.read())
            return """<body style="text-align:center;">
                    <h1>Wallet created!</h1>""" + "<br><br><p>Your login - </p>" + login + "<br><br><p>Your password - </p>" + password + "<br><br><p>Your address - </p>" + address + """
                    <a href="/"><p>Sign in</p></a>"""
            pass



@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        address = request.form.get("address")
        gen = sha256(str(password+login).encode('utf-8')).hexdigest()
        check = gen
        if check == address:
            frec = open(address + ".txt", "r")
            balance = float(frec.read())
            return """<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Good!</title>
</head>
<body style="text-align:center;">"""+ "Your login - " + str(login) + "<br>" + "Your password - " + str(password) + "<br>" + "Your address - " + str(address) + "<br>" + "Your DROM balance - " + str(balance) + "<br>" + "<br>" + """<h1 style="text-align: center;margin-top: 5%">Send coins!</h1>
    <form action="/transaction" style="text-align: center;" method="post">
    <h2 style="text-align: center;">Confirm your address:</h2>
        <input type="text" name="address">
        <br>
        <br>
    <h2 style="text-align: center;">Confirm your login:</h2>
        <input type="text" name="login">
        <br>
        <br>
    <h2 style="text-align: center;">Confirm your password:</h2>
        <input type="text" name="password">
        <br>
        <br>
    <h2 style="text-align: center;">Type receiver address:</h2>
        <input type="text" name="receiver">
        <br>
        <br>
    <h2 style="text-align: center;">Type amount of coins:</h2>
        <input type="text" name="amount">
        <input type="submit" value="Send">
    </form>
    
    <h1 style="text-align: center;margin-top: 5%">Check address!</h1>
    <form action="/address_check" style="text-align: center;" method="post">
    <h2 style="text-align: center;">Type address:</h2>
        <input type="text" name="address">
        <input type="submit" value="Check">
    </form>
    
    <h1 style="text-align: center;margin-top: 5%">Check transaction!</h1>
    <form action="/tr_check" style="text-align: center;" method="post">
    <h2 style="text-align: center;">Type hash (with trx_):</h2>
        <input type="text" name="hash">
        <input type="submit" value="Check">
    </form>
    
    <h1 style="text-align: center;margin-top: 5%">Generate coins!</h1>
    <form action="/miner" style="text-align: center;" method="post">
    <h2 style="text-align: center;">Type address:</h2>
        <input type="text" name="address">
        <input type="submit" value="Generate">
    </form>
    </body>
            </html>"""
        else:
            return """<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Fail</title>
</head>
<body style="text-align:center;">""" + "Your login - " + str(login) + "<br>" + "Your password - " + str(password) + "<br>" + "Your address - " + str(address) + "<br>" + "<h1>Fail!</h1>"


@app.route('/miner', methods=["GET", "POST"])
def mining_l():
    if request.method == "POST":
        reward = 0.001
        address = request.form.get("address")
        frec = open(address + ".txt", "r")
        balance = float(frec.read())
        rewarded_balance = balance + reward
        with open(address + ".txt", 'w') as e:
            e.write(str(rewarded_balance))
            balance = rewarded_balance
        return """<body style="text-align:center;">"""+"<h1>Coins generated!</h1>"+"<br><br><p>Address - </p>"+address+"<br><br><p>New address balance - </p>"+str(balance)+" DROM"


@app.route('/tr_check', methods=["GET", "POST"])
def trx_check():
    if request.method == "POST":
        hash = request.form.get("hash")
        frec = open(hash + ".txt", "r")
        info = frec.read()
        return """<body style="text-align:center;">"""+"<h1>Transaction info:</h1>"+"<br><br>"+info+"""</body>"""


@app.route('/address_check', methods=["GET", "POST"])
def addcheck():
    if request.method == "POST":
        address = request.form.get("address")
        frec = open(address + ".txt", "r")
        balance = float(frec.read())
        return """<body style="text-align:center;">"""+"<h1>Address info</h1>"+"<br><br><p>Address - </p>"+address+"<br><br><p>Address balance - </p>"+str(balance)+" DROM"


@app.route('/transaction', methods=["GET", "POST"])
def trx():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        address = request.form.get("address")
        receiver = request.form.get("receiver")
        amount = request.form.get("amount")
        gen = sha256(str(password+login).encode('utf-8')).hexdigest()
        check = gen
        if check == address:
            try:
                frec = open(address + ".txt", "r")
                balance = float(frec.read())
                amnt = float(amount)
                if amnt < 0:
                    return "<h1>Fail</h1>"
                if amnt > balance:
                    return "<h1>Fail</h1>"
                else:
                    if amnt < 0:
                        return "<h1>Fail</h1>"
                    else:
                        frecr = open(receiver + ".txt", "r")
                        balance_receiver = float(frecr.read())
                        sending = balance - amnt
                        receiving = balance_receiver + amnt
                        with open(receiver + ".txt", 'w') as e:
                            e.write(str(receiving))
                        with open(address + ".txt", 'w') as ios:
                            ios.write(str(sending))
                        letters = string.ascii_letters
                        random_str = ''.join(random.choice(letters) for i in range(33))
                        trxhash = sha256(str(address+receiver+amount+random_str).encode('utf-8')).hexdigest()
                        f = open("trx_" + trxhash + ".txt", "w")
                        if address == receiver:
                            f.write("Address - " + address + " | Burned " + str(amount) + " DROM")
                        else:
                            f.write("Address - " + address + " | Send - " + str(amount) + " DROM | To - " + receiver)
                        return """<body style="text-align:center;">
                        <h1>Transaction successfully!</h1>
                        <br>
                        <br>"""+"Your address - "+address+"<br><br>"+"Receiver address - "+receiver+"<br><br>"+"Amount - "+amount+" DROM"+"<br><br>"+"Hash - trx_"+ trxhash+ """</body>"""
            except Exception:
                return "<h1>Error</h1>"
                pass
        else:
            return """<h1>Transaction Failed</h1>"""


if __name__ == "__main__":
    app.run(debug=True)