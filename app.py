import os
from bottle import run, template, route

@route('/')
def index():
    return "Hello World"

def main():
    port = os.getenv('PORT', '3000')
    run(host="localhost", port=int(port))

main()