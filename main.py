import random
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import create_db, get_player, create_player, update_guess, get_leaderboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(
    title="🎯 Number Guessing Game",
    description="Register a username, then guess your secret number (1–100). Fewest guesses wins!",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------- Request / Response models ----------

class RegisterRequest(BaseModel):
    username: str

class GuessRequest(BaseModel):
    username: str
    guess: int


# ---------- Endpoints ----------

@app.post("/register", summary="Register a new player")
def register(req: RegisterRequest):
    """
    Register with a username. You'll be assigned a secret number between 1 and 100.
    If the username is already taken, you'll get an error.
    """
    username = req.username.strip().lower()
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty.")

    existing = get_player(username)
    if existing:
        raise HTTPException(status_code=409, detail=f"Username '{username}' is already taken.")

    secret = random.randint(1, 100)
    create_player(username, secret)
    return {"message": f"Welcome, {username}! Your secret number is set. Start guessing!", "username": username}


@app.post("/guess", summary="Make a guess")
def guess(req: GuessRequest):
    """
    Submit a guess for your secret number. Returns 'Too high', 'Too low', or 'Correct!'.
    Every attempt (including wrong ones) counts toward your score.
    """
    username = req.username.strip().lower()
    player = get_player(username)

    if not player:
        raise HTTPException(status_code=404, detail=f"Player '{username}' not found. Register first.")
    if player["solved"]:
        raise HTTPException(status_code=400, detail=f"You already solved it in {player['guess_count']} guesses! 🎉")
    if req.guess < 1 or req.guess > 100:
        raise HTTPException(status_code=400, detail="Guess must be between 1 and 100.")

    secret = player["secret_number"]
    new_count = player["guess_count"] + 1

    if req.guess < secret:
        hint = "Too low! 📈"
        solved = False
    elif req.guess > secret:
        hint = "Too high! 📉"
        solved = False
    else:
        hint = f"Correct! 🎯 You got it in {new_count} guess{'es' if new_count != 1 else ''}!"
        solved = True

    update_guess(username, new_count, solved)
    return {"result": hint, "guess_count": new_count, "solved": solved}


@app.get("/leaderboard", summary="See the leaderboard")
def leaderboard():
    """
    Returns all players who have solved their number, ranked by fewest guesses.
    Ties are broken by username alphabetically.
    """
    players = get_leaderboard()
    if not players:
        return {"message": "No players have registered yet.", "leaderboard": []}

    ranked = [
        {
            "rank": i + 1,
            "username": p["username"],
            "guesses": p["guess_count"],
            "solved": bool(p["solved"]),
        }
        for i, p in enumerate(players)
    ]
    return {"leaderboard": ranked}


@app.get("/player/{username}", summary="Check a player's status")
def player_status(username: str):
    """Check how many guesses a player has made and whether they've solved it."""
    player = get_player(username.strip().lower())
    if not player:
        raise HTTPException(status_code=404, detail=f"Player '{username}' not found.")
    return {
        "username": player["username"],
        "guess_count": player["guess_count"],
        "solved": player["solved"],
    }


@app.get("/", summary="Health check")
def root():
    return {"status": "ok", "message": "Guessing game is running. Visit /docs to play!"}