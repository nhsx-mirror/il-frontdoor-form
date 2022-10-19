import os
from bottle import Bottle, run, template, route

application = Bottle()

@application.route('/')
def index():
    return "Hello World"

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()