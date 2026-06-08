# 🎯 Number Guessing Game

## For the host (you)

**Run the server locally:**
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Deploy to Render:**
1. Push this folder to a GitHub repo
2. Go to https://render.com → New → Web Service → connect your repo
3. Render picks up `render.yaml` automatically — click Deploy
4. Share the public URL with players

---

## For players

Install the requests library, then open `solution_template.py`.

```bash
pip install requests
```

Update `BASE_URL` at the top to point at the server, then fill in the two functions:

- `post_guess(username, guess)` — POST to `/guess`, return the response JSON
- `get_leaderboard()` — GET `/leaderboard`, return the response JSON

Run your script:
```bash
python solution_template.py
```

The game loop, binary search strategy, and leaderboard display are all handled for you.
The player with the fewest guesses wins!

---

## Endpoint reference (for players writing their functions)

### POST `/guess`
```
Body:     { "username": "alice", "guess": 50 }
Response: { "result": "Too low! 📈", "guess_count": 1, "solved": false }
```

### GET `/leaderboard`
```
Response: { "leaderboard": [ { "rank": 1, "username": "bob", "guesses": 4 } ] }
```
