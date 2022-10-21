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
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">

    <link href="https://assets.nhs.uk/" rel="preconnect" crossorigin>

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
    <script>document.body.className = ((document.body.className) ? document.body.className + ' js-enabled' : 'js-enabled');</script>
    <a class="nhsuk-skip-link" href="#maincontent">Skip to main content</a>
    
    <header class="nhsuk-header" role="banner">
      <div class="nhsuk-width-container nhsuk-header__container">
        <div class="nhsuk-header__logo nhsuk-header__logo--only"><a class="nhsuk-header__link nhsuk-header__link--service " href="/" aria-label="NHS homepage">
        
          <svg class="nhsuk-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 16" height="40" width="100">
            <path class="nhsuk-logo__background" fill="#005eb8" d="M0 0h40v16H0z"></path>
            <path class="nhsuk-logo__text" fill="#fff" d="M3.9 1.5h4.4l2.6 9h.1l1.8-9h3.3l-2.8 13H9l-2.7-9h-.1l-1.8 9H1.1M17.3 1.5h3.6l-1 4.9h4L25 1.5h3.5l-2.7 13h-3.5l1.1-5.6h-4.1l-1.2 5.6h-3.4M37.7 4.4c-.7-.3-1.6-.6-2.9-.6-1.4 0-2.5.2-2.5 1.3 0 1.8 5.1 1.2 5.1 5.1 0 3.6-3.3 4.5-6.4 4.5-1.3 0-2.9-.3-4-.7l.8-2.7c.7.4 2.1.7 3.2.7s2.8-.2 2.8-1.5c0-2.1-5.1-1.3-5.1-5 0-3.4 2.9-4.4 5.8-4.4 1.6 0 3.1.2 4 .6"></path>
          </svg>

          <span class="nhsuk-header__service-name">
            Innovation Lab Front Door: bring us your ideas!
          </span>
        </div>
      </div>
    </header>
    
    <nav class="nhsuk-breadcrumb" aria-label="Breadcrumb">
      <div class="nhsuk-width-container">
        <ol class="nhsuk-breadcrumb__list">
          <li class="nhsuk-breadcrumb__item"><a class="nhsuk-breadcrumb__link" href="/">Home</a></li>
        </ol>
        <p class="nhsuk-breadcrumb__back"><a class="nhsuk-breadcrumb__backlink" href="/">Back to Home</a></p>
      </div>
    </nav>

    <div class="nhsuk-width-container ">
      <main class="nhsuk-main-wrapper " id="maincontent" role="main">
        <div class="nhsuk-grid-row">
          <div class="nhsuk-grid-column-two-thirds">
            {{!body}}
          </div>
        </div>
      </main>
    </div>

    <footer role="contentinfo">
      <div class="nhsuk-footer" id="nhsuk-footer">
        <div class="nhsuk-width-container">
          <h2 class="nhsuk-u-visually-hidden">Support links</h2>
          <ul class="nhsuk-footer__list">
            <li class="nhsuk-footer__list-item"><a class="nhsuk-footer__list-item-link" href="/">Home</a></li>
          </ul>
          <p class="nhsuk-footer__copyright">&copy; Crown copyright</p>
        </div>
      </div>
    </footer>

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