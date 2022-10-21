import os
from bottle import Bottle, run, template, route, redirect
from datetime import datetime
import boto3

application = Bottle()
client = boto3.client('sns', region_name='eu-west-2')

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

thanks_template = """
<!doctype html>
<html>
  <head>

  </head>
  <body>
    <h1>Thanks</h1>
    <a href="/">back</a>
  </body>
</html>
"""

def send_message(isotime):
    msg = f"Test message {isotime}"

    response = client.publish(
        TopicArn='arn:aws:sns:eu-west-2:521826052428:test-topic',
        Message=msg,
        Subject=msg
    )
    print(response)

@application.route('/')
def index():
    return form_template

@application.post('/post')
def send():
    isotime = datetime.now().isoformat()
    send_message(isotime)
    redirect(f'/thanks?isotime={isotime}')

@application.route('/thanks')
def thanks():
    return thanks_template

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()