from flask import Flask, render_template, url_for, request, redirect, flash
import requests
import json
import hashlib

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def name():
	return render_template('index.html')

@app.route('/index')
def nam():
	return render_template('index.html')

@app.route('/message')
def names():
	return render_template('message.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/submit_form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        data = request.form['password']
   
        num = main(data)
        numb = int(num)
        info = {
            "password" : data,
            "count" : numb
        }
        return render_template('message.html', value=info)
    else:
    	return 'bad'



def request_api(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, Try API AGAIN!!')
    return res


def get_leaked(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_pass(passwords):
    sha1pass = hashlib.sha1(passwords.encode('utf-8')).hexdigest().upper()
    first5_char, rest = sha1pass[:5], sha1pass[5:]
    response = request_api(first5_char)
    return get_leaked(response, rest)



def main(args):
    count = pwned_pass(args)
    if count:
        message = (f'''
            Password ""{args}"" has been Hacked {count} times...
                    Try a more secure Password!!
        ''')
    else:
        message = (f'''
           Password ""{args}"" Has not been Breached or hacked HOORAY!!! 
                   You can continue with this password!!
        ''')
    return count