# -*- coding: utf-8 -*-
    
from flask import Flask
from flask import Response
from flask import stream_with_context

import requests

app = Flask(__name__)

ports = {
'annot': 24000,
'img_server': 24001,
'arxiv': 22000, 
'blog': 8080,
'ipynb': 8081,
'ipynb_remeo': 21001
}

def url_mapping(url):
    url_sp = url.split('/')
    if url_sp[0] in ports:
        port = ports[url_sp[0]]
    else:
        return url
    rest = '/'.join(url_sp[1:])
    url = 'http://localhost:{}/{}'.format(port, rest)
    return url

@app.route('/favicon.ico')
def icon():
    return ''

@app.route('/<path:url>')
def home(url):
    url_orig = url
    url = url_mapping(url)
    print('Given url : {}, Transformed url : {}'.format(url_orig, url))
    req = requests.get(url, stream = True)
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
