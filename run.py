import os
from flask import Flask, redirect, render_template, request
from datetime import datetime

app = Flask(__name__)


def write_to_file(filename, data):
    with open(filename, 'a') as file:
        file.writelines(data)

def get_all_comments():
    comments = []
    with open('data/comments.txt', 'r') as prob_comments:
        comments = prob_comments.readlines()
    return comments
    
def add_comments(username, comment):
    write_to_file('data/comments.txt', "({0}) {1} - {2}\n".format(
            datetime.now().strftime("%H:%M"),
            username,
            comment))
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        write_to_file('data/users.txt', request.form['username'] + '\n')
        return redirect(request.form['username'])
    return render_template('index.html')
    
@app.route('/<username>')
def user(username):
    comments = get_all_comments()
    return render_template('log.html', username=username, prob_comments=comments)
    
@app.route('/<username>/<comment>')
def send_comment(username, comment):
    add_comments(username, comment)
    return redirect(username)
    
    
        
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)            