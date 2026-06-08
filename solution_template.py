import requests

BASE_URL = "https://your-app.onrender.com"  # replace with your deployed URL

# ================================================================
# YOUR TASKS — fill in these two functions only
# ================================================================

def post_guess(username: str, guess: int) -> dict:
    """
    Make a POST request to /guess with the username and guess.
    Return the response as a dict.

    The endpoint expects:
        POST /guess
        { "username": "alice", "guess": 50 }

    It returns something like:
        { "result": "Too low! 📈", "guess_count": 1, "solved": false }
    """
    # YOUR CODE HERE
    pass


def get_leaderboard() -> dict:
    """
    Make a GET request to /leaderboard.
    Return the response as a dict.

    It returns something like:
        {
          "leaderboard": [
            { "rank": 1, "username": "bob", "guesses": 4 },
            { "rank": 2, "username": "alice", "guesses": 7 }
          ]
        }
    """
    # YOUR CODE HERE
    pass


# ================================================================
# Everything below is already written — don't change it
# ================================================================

def register(username: str):
    resp = requests.post(f"{BASE_URL}/register", json={"username": username})
    data = resp.json()
    if resp.status_code != 200:
        print(f"Error: {data.get('detail')}")
        exit(1)
    print(data["message"])


def play(username: str):
    """Binary search guessing loop — runs until the number is found."""
    low, high = 1, 100
    print(f"\nGuessing your number between {low} and {high}...\n")

    while True:
        guess = (low + high) // 2
        print(f"  Guessing {guess}...", end=" ")

        result = post_guess(username, guess)

        if result is None:
            print("\npost_guess() returned None — did you forget to return the response?")
            exit(1)

        print(result["result"])

        if result["solved"]:
            print(f"\n🎉 Done! Found in {result['guess_count']} guesses.")
            break

        if "Too low" in result["result"]:
            low = guess + 1
        elif "Too high" in result["result"]:
            high = guess - 1


def show_leaderboard():
    print("\n🏆 Leaderboard\n" + "-" * 30)

    data = get_leaderboard()

    if data is None:
        print("get_leaderboard() returned None — did you forget to return the response?")
        return

    board = data.get("leaderboard", [])
    if not board:
        print(data.get("message", "No results yet."))
        return

    for entry in board:
        print(f"  #{entry['rank']}  {entry['username']:<20} {entry['guesses']} guesses")


if __name__ == "__main__":
    username = input("Enter your username: ").strip()
    register(username)
    play(username)
    show_leaderboard()
