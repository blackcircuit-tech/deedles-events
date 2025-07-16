import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect
import uuid

print(" Flask has started — you're running app.py")

app = Flask(__name__)
REVIEW_FILE = "reviews.txt"

# ========== Review Functions ==========
def load_reviews():
    if not os.path.exists(REVIEW_FILE):
        return []
    with open(REVIEW_FILE, "r") as file:
        lines = file.readlines()
        reviews = []
        for line in lines:
            parts = line.strip().split(":::", 2)
            if len(parts) == 3:
                reviews.append({"id": parts[0], "name": parts[1], "message": parts[2]})
        return reviews

def save_review(name, message):
    review_id = str(uuid.uuid4())
    with open(REVIEW_FILE, "a") as file:
        file.write(f"{review_id}:::{name}:::{message}\n")

def delete_review(review_id):
    reviews = load_reviews()
    new_reviews = [r for r in reviews if r["id"] != review_id]
    with open(REVIEW_FILE, "w") as file:
        for r in new_reviews:
            file.write(f'{r["id"]}:::{r["name"]}:::{r["message"]}\n')

# ========== Routes ==========
@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        save_review(name, message)
        return redirect("/reviews")
    all_reviews = load_reviews()
    return render_template("reviews.html", reviews=all_reviews)

@app.route("/delete_review/<review_id>")
def delete_review_route(review_id):
    delete_review(review_id)
    return redirect("/reviews")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Email content
        full_message = f"New message from {name} ({email}):\n\n{message}"
        msg = MIMEText(full_message)
        msg["Subject"] = "New Contact Form Message - Deedles Events"
        msg["From"] = "mwansapatricia381@gmail.com"
        msg["To"] = "mwansapatricia381@gmail.com"

        # Gmail SMTP setup
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("mwansapatricia381@gmail.com", "rsxkoqrkokdsjurt")  # your app password
            smtp.send_message(msg)

        return redirect("/contact")

    return render_template("contact.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/test")
def test():
    return "You are running the real app.py!"

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)