from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc
import os

# imports from other python files (i.e. Functions and Variables)
from user_conditions import username_conditions, invalid_username_conditions, password_conditions, invalid_password_conditions
from condition_functions import check_username_conditions, check_password_conditions
from test17 import api_calls, preview_database, query_database
#from queryDatabase import query_database

app = Flask(__name__)

app.secret_key = os.urandom(24)
apiKey = 'RGAPI-6ed553fd-6357-4822-ad46-4d96813d69a6'
region = 'na1'
participants = 'AYD Trash', 'AYD Anarchy'
summonerName = participants[0]
# connects to database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

def matchCount(league_account):
    # SQL query to find number of matches league_account played
    cursor.execute("SELECT COUNT(*) FROM dbo.Participants where summonerName = ?", league_account)

    # Fetch the results
    matches = cursor.fetchall()

    print(matches)

    return matches


 # SQL query to find the winrate of two players when playing togeather (non rounded)

def winRate(league_account):
    cursor.execute('''
        SELECT 
            (COUNT(CASE WHEN p1.teamID = m.matchResult THEN 1 END) * 100.0) / NULLIF(COUNT(*), 0) as winrate_percentage
        FROM Participants p1
        INNER JOIN Matches m ON p1.matchID = m.matchID
        WHERE p1.summonerName = ?
    ''', league_account)

    winrate_solo = cursor.fetchall()

    return winrate_solo


def killDeathAssist(league_account):
    #SQL query to find the average KDA of both players
    cursor.execute('''
        SELECT 
        AVG(p.kda) as avg_kda
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', league_account)

    avg_kda = cursor.fetchall()

    return avg_kda

def killParticipation(league_account):
    #SQL query to find the average KDA of both players
    cursor.execute('''
        SELECT 
        AVG(p.killParticipation) as kill_participation
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', league_account)

    kill_participation = cursor.fetchall()

    return kill_participation

def avgDamageDealtToChampions(league_account):
    #SQL query to find the average KDA of both players
    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions) as avg_total_damage_dealt_to_champions
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', league_account)

    avg_damage_dealt_to_champions = cursor.fetchall()

    return avg_damage_dealt_to_champions

def avgDamageDealtPerMinute(league_account):
    #SQL query to find the average KDA of both players
    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions * 60.0 / m.matchDuration) as avg_damage_dealt_per_minute 
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', league_account)

    avg_damage_dealt_per_minute = cursor.fetchall()

    return avg_damage_dealt_per_minute 

def create_users_table():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE Users (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            Username NVARCHAR(80) NOT NULL,
            Email NVARCHAR(120) NOT NULL,
            Password NVARCHAR(80) NOT NULL,
            Gamertag NVARCHAR(80)
        );
    ''')
    conn.commit()
     
def initialize_database():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users';")
    if cursor.fetchone()[0] == 0:
        create_users_table()

initialize_database()

@app.route("/home")
def home():
    if 'logged_in' in session and session['logged_in']:
        league_account = session.get('username', None)
        return render_template('home.html', username=league_account)
    else:
        return render_template('home.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)  # Optional: remove the username from session
    return redirect(url_for('home'))

@app.route("/about")
def about():
    if 'logged_in' in session and session['logged_in']:
        league_account = session.get('username', None)
        return render_template('about.html', username=league_account)
    else:
        return render_template('about.html')

@app.route("/account")
def account():
    if 'logged_in' in session and session['logged_in']:
        username = session.get('username', None)
        email = session.get('email', None)
        gamertag = session.get('league_account', None)
        return render_template('account.html', username=username, email=email, gamertag=gamertag)
    else:
        return render_template('account.html')

# app route renders the template with methods GET and POST
# Get is the method that allows the user information to be obtained from the html form
@app.route("/signup", methods=['GET', 'POST'])
def signup():

    # Method that runs when signup form is submitted
    if request.method == 'POST':

        # Retrieves user inputs and assigns them to variables
        username = request.form['username']
        password = request.form['password']
        gamertag = request.form['gamertag']
        email = request.form['email']

        # if satement that determines what section is incorrect and re
        if check_username_conditions(username) == False:
            if check_password_conditions(password) == False:
                return render_template('signup.html', username_conditions=invalid_username_conditions, password_conditions=invalid_password_conditions)
            else:
                return render_template('signup.html', username_conditions=invalid_username_conditions, password_conditions=password_conditions)
        elif check_password_conditions(password) == False:
            return render_template('signup.html', username_conditions=username_conditions, password_conditions=invalid_password_conditions)
        else:
            # SQL query that inputs the users data into the database
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (Username, Email, Password, Gamertag) VALUES (?, ?, ?, ?)", (username, email, password, gamertag))
            conn.commit()
            
            return render_template('login.html')
    else:
        return render_template('signup.html', username_conditions=username_conditions, password_conditions=password_conditions)

# app route renders the template with methods GET and POST
# Get is the method that allows the user information to be obtained from the html form
@app.route('/login', methods=['GET', 'POST']) 
def login():  
    # Method that runs when login form is submitted     
    if request.method == 'POST':          # Retrieves user username input and saves it to variables         
        username = request.form['username']         
        password = request.form['password']          
        # SQL query that retrieves the users username and password from the database         
        # # Retrieves encoded password from database and returns hex string         
        cursor = conn.cursor()         
        cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))         
        user = cursor.fetchone()          
        
        cursor.execute("SELECT username, password, email, gamertag FROM users WHERE Username = ? AND Password = ?", (username, password))         
        result = cursor.fetchall()         
        if user: 
                       
            session['logged_in'] = True             
            session['email'] = result[0][2]             
            session['username'] = result[0][0]             
            session['league_account'] = result[0][3]
                # Other session setup
            return render_template('loading.html', username=username)  # Render loading page
        else:
            error_message = "Username and/or Password is incorrect. Please enter a valid Username and/or Password."
            return render_template('login.html', error_message=error_message)
    else: 
        error_message = ""
        return render_template('login.html', error_message=error_message)


@app.route("/lookup_duo")
def lookup_duo():
    if 'logged_in' in session and session['logged_in']:
        league_account = session.get('username', None)
        return render_template('lookup_duo.html', username=league_account)
    else:
        return render_template('lookup_duo.html')

@app.route("/lookup_team")
def lookup_team():
    if 'logged_in' in session and session['logged_in']:
        league_account = session.get('username', None)
        return render_template('lookup_team.html', username=league_account)
    else:
        return render_template('lookup_team.html')

@app.route("/self_stat")
def self_stat():
    if 'logged_in' in session and session['logged_in']:
        league_account = session.get('league_account', None)
        username = session.get('username', None)
        # Fetch user data from your database
        matches = matchCount(league_account)
        win_rate = winRate(league_account)
        avg_kda = killDeathAssist(league_account)
        kill_participation = killParticipation(league_account)
        avg_damage_dealt_to_champions = avgDamageDealtToChampions(league_account)
        avg_damage_dealt_per_minute = avgDamageDealtPerMinute(league_account)

        if avg_damage_dealt_per_minute:
            avg_damage_dealt_per_minute = avg_damage_dealt_per_minute[0][0]
        else:
            avg_damage_dealt_per_minute = 0

        if avg_damage_dealt_to_champions:
            avg_damage_dealt_to_champions = avg_damage_dealt_to_champions[0][0]
        else:
            avg_damage_dealt_to_champions = 0
        

        if kill_participation:
            kill_participation = kill_participation[0][0]
        else:
            kill_participation = 0
        if avg_kda:
            avg_kda = avg_kda[0][0]
        else:
            avg_kda = 0 

        if win_rate:
            win_rate = win_rate[0][0]
        else:
            win_rate = 0 

        if matches:
            games_played = matches[0][0]
        else:
            games_played = 0  # or any default value
        
        return render_template('self_stat.html', username=username, league_account=league_account, games_played=games_played, win_rate= round(win_rate,2), avg_kda= round(avg_kda,2), kill_participation= round(kill_participation,2), avg_damage_dealt_to_champions=avg_damage_dealt_to_champions, avg_damage_dealt_per_minute=round(avg_damage_dealt_per_minute,2))
    else:
        return render_template('self_stat.html')




@app.route("/loading")
def loading():
    return render_template('loading.html')

@app.route('/process_login/<username>')
def process_login(username):
    # Move your background functions here
    api_calls(summonerName, region, apiKey)
    preview_database()
    query_database()
    return redirect(url_for('home'))\

if __name__ == '__main__':
    app.secret_key = app.secret_key
    app.run(debug=True)