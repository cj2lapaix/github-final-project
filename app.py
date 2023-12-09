from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['STATIC_FOLDER'] = 'static'
Session(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    return render_template("appointments.html")

@app.route("/registrants")
def registration():
    registrants = session.get("registrants", [])
    return render_template("registrants.html", registrants=registrants)

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        time = request.form.get("Message")
        date = request.form.get("email")
        registrant = {'name': name, 'phone': phone, "Message": time, "email": date}

        # Get the existing registrants from the session or initialize an empty list
        registrants = session.get("registrants", [])

        # Append the new registrant
        registrants.append(registrant)

        # Update the session with the modified list of registrants
        session["registrants"] = registrants

    return render_template("success.html")

@app.route("/deregister", methods=["POST"])
def deregister():
    if request.method == "POST":
        # Get the index of the registrant to be deregistered
        index_to_remove = int(request.form.get("id"))

        # Get the existing registrants from the session or initialize an empty list
        registrants = session.get("registrants", [])

        if 1 <= index_to_remove <= len(registrants):
            # Remove the registrant at the specified index
            removed_registrant = registrants.pop(index_to_remove - 1)

            # Update the session with the modified list of registrants
            session["registrants"] = registrants

            # Optionally, you can use the removed registrant data as needed
            print(f"Deregistered: {removed_registrant}")

    return redirect("/registrants")


@app.route('/clear_session')
def clear_session():
    session.clear()
    return render_template('session_cleared.html')

if __name__ == "__main__":
    app.run(debug=True)
