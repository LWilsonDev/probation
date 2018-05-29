import os
from flask import Flask, redirect, render_template, request
from datetime import datetime
from datetime import timedelta  

app = Flask(__name__)


def write_to_file(filename, data):
    with open(filename, 'a') as file:
        file.writelines(data)

def get_all_comments():
    comments = []
    with open('data/comments.txt', 'r') as prob_comments:
        comments = prob_comments.readlines()[::-1]
    return comments
    
def add_comments(username, comment, days):
    write_to_file('data/comments.txt', "({0}) {1} Days = {2} Reason: {3}\n".format(
            datetime.now().strftime("%H:%M"),
            username,
            days,
            comment))
    return redirect(request.form) 

def get_stored_days():
    with open('data/days.txt', 'r') as current_days:
        stored_days = current_days.read()
        return stored_days
        

    
def overwrite(filename, data):
    with open(filename, 'w+') as file:
        file.writelines(data)    
        

    

        
    
   
        
@app.route('/', methods=['GET', 'POST'])
def index():
    stored_days = get_stored_days()
    date = datetime.now() + timedelta(int(stored_days))
    end_date = date.strftime('%A %d %B %Y')
    if request.method == 'POST':
        write_to_file('data/users.txt', request.form['username'] + '\n')
        return redirect(request.form['username'])
    return render_template('index.html', end_date=end_date)
    
@app.route('/<username>', methods=['GET', 'POST'])
def user(username):
    comments = get_all_comments()
    if request.method == 'POST':
        comment = request.form['comment']
        days = request.form['days']
        add_comments(username, comment, days)
        
        overwrite('data/days.txt', days)
        return redirect(username)
    return render_template("log.html",
                            username=username, prob_comments=comments)
    
    

    
        
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)            