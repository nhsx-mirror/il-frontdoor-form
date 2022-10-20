import os
from bottle import Bottle, run, template, route

application = Bottle()

form_template = """
<!doctype html>
<html>
  <head>

  </head>
  <body>
    <h1>Hello World</h1>
    <form action="/post" method="post">
        <input type="submit" value="Send an email">
    </form>
  </body>
</html>
"""

@application.route('/')
def index():
    return form_template

@application.post('/post')
def send():
    return "thanks"

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()