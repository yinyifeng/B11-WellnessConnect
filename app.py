from flask import Flask, request, render_template, session, redirect, url_for
import psycopg2

app = Flask(__name__)
app.secret_key = 'super-secret-key'

conn = psycopg2.connect(
    dbname="wellnessconnect",
    user="postgres",
    password="sayuri03",
    host="localhost",
    port="5433"
)

@app.route("/homepage")
def homepage():
    try:
        if not session.get("user_id"):
            session["user_id"] = 7 # TEMP: assume you're testing as user_id = 1
        current_user_id = session.get("user_id")
        sort_order = request.args.get("filter", "highest")
        with conn.cursor() as cur:
            if sort_order == "lowest":
                cur.execute("""
                    SELECT username, cumulative_points
                    FROM users
                    ORDER BY cumulative_points ASC
                """)
            else:  # default to highest
                cur.execute("""
                    SELECT username, cumulative_points
                    FROM users
                    ORDER BY cumulative_points DESC
                """)
            rows = cur.fetchall()
            leaderboard_data = [
                {"rank": idx + 1, "username": row[0], "points": int(row[1])}
                for idx, row in enumerate(rows)
            ]
            cur.execute("SELECT available_points FROM users WHERE user_id = %s", (current_user_id,))
            result = cur.fetchone()
            current_user_points = result[0] if result else 0
            percentage = min(current_user_points / 1000 * 100, 100)
            return render_template(
                "homepage.html",
                leaderboard=leaderboard_data,
                percentage=percentage,
                current_user_points=current_user_points,
                current_filter=sort_order 
            )  
    except Exception as e:
        print("Leaderboard error:", e)
        return f"Error: {str(e)}", 500
    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

