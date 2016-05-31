# -*- coding: utf-8 -*-
import socket

from flask import Flask
from flask import Response
from flask import stream_with_context
from flask import redirect

app = Flask(__name__)

ports = {
    'annot': '{host}:20000',
    'arxiv': '{host}:20001', 
    'ipynb_romeo': '{host}:20002',
    'img_server' : '{host}:5001',
    'ipynb': '{host}:8081',
}

def get_hostname():
    hostname = socket.gethostname()
    return hostname

def url_mapping(url):
    url_sp = url.split('/')
    if url_sp[0] in ports:
        port = ports[url_sp[0]]
    else:
        return url
    rest = '/'.join(url_sp[1:])
    host = get_hostname()
    url = 'http://{}/{}'.format(port, rest).format(host=host)
    return url

@app.route('/favicon.ico')
def icon():
    return ''

@app.route('/<path:url>')
def home(url):
    url_orig = url
    url = url_mapping(url)
    print('Given url : {}, Transformed url : {}'.format(url_orig, url))
    return redirect(url, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
