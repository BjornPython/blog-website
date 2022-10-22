from flask import Flask, render_template, request
import requests
import smtplib
import ssl
from email.message import EmailMessage
import os

app = Flask(__name__)

my_email = os.environ.get("MY_EMAIL")
my_pass = os.environ.get("MY_PASS")
email_receiver = "nathanflores887@gmail.com"


# ----------- FUNCTIONS ----------------------#
def send_email(username, email, number, message, recipient):
    """Emails me when a user contacts me in my webpage."""
    em = EmailMessage()
    em["From"] = my_email
    em["Subject"] = f"{username} sent you a message"
    body = f"{message}, EMAIL: {email}, PHONE NUMBER: {number}"
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as connection:
        connection.login(my_email, my_pass)
        connection.sendmail(my_email,
                            recipient,
                            em.as_string()
                            )


def get_blogs():
    """Gets the blogs from my custom api from n:point. """
    response = requests.get(url="https://api.npoint.io/ecf4c251492aaabd12b9")
    return response.json()


# ----------- PAGES ----------------------#
@app.route('/')
def home():
    """The home page of the website."""
    blogs = get_blogs()
    return render_template("index.html", blogs=blogs)


@app.route('/about')
def about_me():
    """The about me page of my website"""
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """The contact me page of the website. Gets
    the information the user inputs and calls the
    function send_email to send me the user's message."""
    if request.method == "POST":
        data = request.form
        username = data["username"]
        email = data["email"]
        number = data["number"]
        message = data["message"]
        send_email(username, email, number, message, email_receiver)
        print("hmm")
        return render_template("contact.html", msg_sent=True)
    print("hmm2")
    return render_template("contact.html", msg_sent=False)


@app.route('/blogs/<index>')
def blogs(index):
    """Shows the complete blog content when
    the user clicks a blog in the home page."""
    blogs = get_blogs()
    blog = blogs[int(index) - 1]
    return render_template("post.html", blog=blog)


if __name__ == "__main__":
    app.run(debug=True)
