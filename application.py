import os
from bottle import Bottle, run, template, route, redirect, static_file
from datetime import datetime
import boto3

application = Bottle()
client = boto3.client('sns', region_name='eu-west-2')

form_template = """
<!doctype html>
<html>
  <head>
    <!-- Styles -->
    <link rel="stylesheet" href="/static/css/nhsuk-6.1.2.min.css">

    <!-- Scripts -->
    <script src="/static/js/nhsuk-6.1.2.min.js" defer></script>

    <!-- Favicons -->
    <link rel="shortcut icon" href="/static/assets/favicons/favicon.ico" type="image/x-icon">
    <link rel="apple-touch-icon" href="/static/assets/favicons/apple-touch-icon-180x180.png">
    <link rel="mask-icon" href="/static/assets/favicons/favicon.svg" color="#005eb8">
    <link rel="icon" sizes="192x192" href="/static/assets/favicons/favicon-192x192.png">
    <meta name="msapplication-TileImage" content="/static/assets/favicons/mediumtile-144x144.png">
    <meta name="msapplication-TileColor" content="#005eb8">
    <meta name="msapplication-square70x70logo" content="/static/assets/favicons/smalltile-70x70.png">
    <meta name="msapplication-square150x150logo" content="/static/assets/favicons/mediumtile-150x150.png">
    <meta name="msapplication-wide310x150logo" content="/static/assets/favicons/widetile-310x150.png">
    <meta name="msapplication-square310x310logo" content="/static/assets/favicons/largetile-310x310.png">
  </head>
  <body>
    {{!body}}
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
    return template(form_template, body="""
    <h1>Hello World</h1>
    <form action="/post" method="post">
        <input type="submit" value="Send an email">
    </form>
    """)

@application.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static/')

@application.post('/post')
def send():
    isotime = datetime.now().isoformat()
    send_message(isotime)
    redirect(f'/thanks?isotime={isotime}')

@application.route('/thanks')
def thanks():
    return template(form_template, body="""
    <h1>Thanks</h1>
    <a href="/">back</a>
    """)

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()