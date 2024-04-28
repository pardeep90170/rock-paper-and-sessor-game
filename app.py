from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session

choices = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

def play_game(user_choice):
    if user_choice not in choices:
        return "Invalid input. Please enter 'rock', 'paper', or 'scissors'."

    computer_choice = random.choice(list(choices.keys()))

    if user_choice == computer_choice:
        result = "It's a draw!"
    elif choices[user_choice] == computer_choice:
        result = "You win!"
    else:
        result = "Computer wins!"

    return {
        "user_choice": user_choice.capitalize(),
        "computer_choice": computer_choice.capitalize(),
        "result": result
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    user_choice = request.form.get("choice")
    game_result = play_game(user_choice)

    # Update score
    session["user_score"] = session.get("user_score", 0)
    session["computer_score"] = session.get("computer_score", 0)
    if game_result["result"] == "You win!":
        session["user_score"] += 1
    elif game_result["result"] == "Computer wins!":
        session["computer_score"] += 1

    return render_template("result.html", **game_result, user_score=session["user_score"], computer_score=session["computer_score"])

if __name__ == "__main__":
    app.run(debug=True)
