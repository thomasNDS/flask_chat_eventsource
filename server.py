#!/usr/bin/env python
import redis
import datetime
from flask import (Flask, request, session, redirect, Response,
                   render_template)


red = redis.StrictRedis()
app = Flask(__name__)
app.secret_key = 'blablabla'


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('chat')
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        return redirect('/')
    return '<form action="" method="post">user: <input name="user"/></form>'


@app.route('/post', methods=['POST'])
def post():
    message = request.form['message']
    user = session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    print message
    red.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return ""


@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/')
def chatroom_test():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html.jinja2', user=session['user'])


if __name__ == '__main__':
    host, port = "127.0.0.1", 5001
    app.run(host=host, port=port, threaded=True)
