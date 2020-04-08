from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import datetime

app = Flask(__name__)

bookmarks = []

app.config['SECRET_KEY'] = b'j\xd3|\x7fb\xc4\x9b\x9e\x90Q\xab\xdb\x0e\xe1S)m{\xf3\t\xaf\xaa{\x9d'

def store_bookmarks(url):
    bookmarks.append(dict(url = url, user = "gbrethen", date = datetime.now()))

class User:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName
    
    def initials(self):
        return "{}. {}.".format(self.firstName[0], self.lastName[0])

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', title="Title passed from view to template", user=User("Greg", "Brethen"))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        url = request.form['url']
        store_bookmarks(url)
        flash(f"stored url: {url}")
        return redirect(url_for('index'))
    return render_template('add.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=False)