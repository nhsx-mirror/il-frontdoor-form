import os
from bottle import Bottle, run, template, route
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

def send_message():
    msg = f"Test message {datetime.now().isoformat()}"

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
    send_message()
    redirect('/thanks')

@application.route('/thanks')
def thanks():
    return thanks_template

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()