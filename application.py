import os
from bottle import Bottle, run, template, route, redirect, static_file, request
from datetime import datetime
import boto3
from random import randint

application = Bottle()
client = boto3.client('sns', region_name='eu-west-2')

def html_form_group(content):
    return f"""
    <div class="nhsuk-form-group">
      {content}
    </div>
    """
def html_fieldset(content):
    return f"""
    <fieldset class="nhsuk-fieldset">
      {content}
    </fieldset>
    """

def html_text_input(name, label):
    return html_form_group(f"""
      <label class="nhsuk-label" for="{name}">
        {label}
      </label>
      <input class="nhsuk-input" id="{name}" name="{name}" type="text">
    """)

def html_text_area(name, label, hint=None):
    html_label = f"""
      <label class="nhsuk-label" for="{name}">
        {label}
      </label>
    """
    html_hint = f"""
      <div class="nhsuk-hint" id="{name}-hint">
        Do not include personal or financial information, for example, your National Insurance number or credit card details.
      </div>
    """ if hint else ""

    html_textarea = f"""
      <textarea class="nhsuk-textarea" id="{name}" name="{name}" rows="5" aria-describedby="{name}-hint"></textarea>
    """

    return html_form_group(html_label + html_hint + html_textarea)

def html_radio_item(name, value, label):
    input_id = f"{name}-{randint(1, 1000000)}"

    return f"""
      <div class="nhsuk-radios__item">
        <input class="nhsuk-radios__input" id="{input_id}" name="{name}" type="radio" value="{value}">
        <label class="nhsuk-label nhsuk-radios__label" for="{input_id}">
          {label}
        </label>
      </div>
    """

def html_legend(legend):
    return f"""
    <legend class="nhsuk-fieldset__legend nhsuk-fieldset__legend--s">
      {legend}
    </legend>
    """

def html_radios(name, legend, options):
    html_options = '<div class="nhsuk_radios">' +\
        "\n".join([html_radio_item(name, o['value'], o['label']) for o in options]) +\
        '</div>'

    return html_form_group(html_fieldset(html_legend(legend) + html_options))

def html_checkbox_item(name, value, label):
    return f"""
      <div class="nhsuk-checkboxes__item">
        <input class="nhsuk-checkboxes__input" id="{name}" name="{name}" type="checkbox" value="{value}">
        <label class="nhsuk-label nhsuk-checkboxes__label" for="{name}">
          {label}
        </label>
      </div>
    """

def html_checkbox(name, value, label, hint=None):
    html_hint = f"""
      <div class="nhsuk-hint" id="{name}-hint">
        {hint}
      </div>
    """ if hint else ''

    return html_form_group(html_fieldset(f"""
      {html_hint}
      <div class="nhsuk-checkboxes">
        {html_checkbox_item(name, value, label)}
      </div>"""))

def html_checkboxes(name, legend, options):
    html_options = '<div class="nhsuk_checkboxes">' +\
        "\n".join([html_checkbox_item(name, o['value'], o['label']) for o in options]) +\
        '</div>'

    return html_form_group(html_fieldset(html_legend(legend) + html_options))

page_template = """
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

form_template=f"""
<h1>Let us help</h1>

<form action="/post" method="post">
  <p>
    Our roadmap is shaped by real challenges and ideas from the health and social care system, and we want to hear from anyone working within it.
    If you have a challenge or idea that you think could be answered with innovative thinking and technology, but you aren't sure exactly how, we'd love to hear about it.  
  </p>

  <p>
    Anyone working within the English health and social care system is eligible to submit.
  </p>

  <p>
    Please note that we don't take submissions relating to existing solutions or products.
    Please see our 
    <a href="https://www.nhsx.nhs.uk/nhsx-innovation-lab/send-us-your-challenges/">
      guidance
    </a>
    on what challenges are/aren't suitable.
  </p>

  <p>
    All submissions will be handled in accordance with the
    <a href="https://www.nhsx.nhs.uk/privacy-policy">
      NHSX data protection policy.
    </a>
    Please do not include any confidential or patient information.
  </p>

  {html_text_input('email', 'What is your email address?')}
  {html_text_input('role', 'What is your role?')}
  {html_text_input('place_of_work', 'What is your place of work?')}
  {html_text_area('challenge', 'In 100 words or less, describe the challenge.')}
  {html_text_area('problem_impact', 'In 100 words or less, describe the impact on patients and/or staff.')}
  {html_text_area('current', 'In 100 words or less, describe what is currently being done to help ease this problem.')}
  {html_text_area('solution_impact', 'In 100 words or less, describe the impact of solving this challenge.')}
  {html_checkbox('has_idea', 'true', 'Click if you have an idea that could help solve this challenge.')}
  {html_text_area('idea', 'What is your idea?')}
  {html_checkbox('has_been_tested', 'true', 'Click if your idea has been tested before.')}
  {html_text_area('evidence', 'What evidence, if any, do you have that your idea would help?')}
  {html_checkboxes('focus_areas', 'Which of our focus areas does the problem apply to?',
    [{'value': 'burden', 'label': 'Reduce the burden on staff'},
     {'value': 'info', 'label': 'Help access clinical information'},
     {'value': 'productivity', 'label': 'Improve health and care productivity'},
     {'value': 'access', 'label': 'Provide tools to access services directly'},
     {'value': 'safety', 'label': 'Improve safety across health and care systems'}])}
  {html_radios('involvement', 'If we pursue this problem, how involved would you like to be?',
    [{'value': 'not', 'label': 'I just want to submit a problem'},
     {'value': 'up_to_date', 'label': 'Keep me up to date on progress'},
     {'value': 'involve', 'label': "Involve me when I'm needed"},
     {'value': 'heavily', 'label': "I'd like to be heavily involved"}])}
  {html_radios('can_test', 'If you work in a care setting, could we test any solutions with you?',
     [{'value': 'yes', 'label': 'Yes'},
      {'value': 'maybe', 'label': 'Maybe'},
      {'value': 'no', 'label': 'No'},
      {'value': 'not_care', 'label': "I don't work in a care setting"}])}
  {html_checkbox('consent', 'true', 'Click here to agree', 
    hint='Your personal data will be stored in compliance with the NHSX Privacy Policy.  It will be used for the purposes of evaluating the information you send us, which may include contacting you in the future to discuss this challenge or other related challenges.  We may also invite you to anonymously provide feedback on your experience in order to improve this service. Please address any data protection requests to <a href="mailto:innovation-lab@nhsx.nhs.uk">innovation-lab@nhsx.nhs.uk</a>.')}
  <input type="submit" class="nhsuk-button" value="Submit">
</form>
"""

email_template = """
Front Door Challenge Submission
===============================

What is your email address?
---------------------------
{{email}}

What is your role?
------------------
{{role}}

What is your place of work?
---------------------------
{{place_of_work}}

In 100 words or less, describe the challenge.
---------------------------------------------
{{challenge}}

In 100 words or less, describe the impact of solving this challenge.
--------------------------------------------------------------------
{{solution_impact}}

Do you have an idea that could help solve this challenge?
---------------------------------------------------------
{{has_idea}}

What is your idea?
------------------
{{idea}}

Has your idea been tested before?
---------------------------------
{{has_been_tested}}

What evidence, if any, do you have that your idea would help?
-------------------------------------------------------------
{{evidence}}

Which of our focus areas does the problem apply to?
---------------------------------------------------
{{focus_areas}}

If we pursue this problem, how involved would you like to be?
-------------------------------------------------------------
{{involvement}}

If you work in a care setting, could we test any solutions with you?
--------------------------------------------------------------------
{{can_test}}
"""

def render_email(params):
    return template(email_template,
      email=params.get('email'),
      role=params.get('role'),
      place_of_work=params.get('place_of_work'),
      challenge=params.get('challenge'),
      solution_impact=params.get('solution_impact'),
      has_idea='Yes' if params.get('has_idea') == 'true' else 'No',
      idea=params.get('idea'),
      has_been_tested='Yes' if params.get('has_been_tested') == 'true' else 'No',
      evidence=params.get('evidence'),
      focus_areas=", ".join(params.getall('focus_areas')),
      involvement=params.get('involvement'),
      can_test=params.get('can_test'))

def send_message(params):
    isotime = datetime.now().isoformat()
    subj = f"Front door submission at {isotime}"
    msg = render_email(request.params)

    response = client.publish(
        TopicArn='arn:aws:sns:eu-west-2:521826052428:test-topic',
        Message=msg,
        Subject=subj
    )
    print(response)

@application.route('/')
def index():
    return template(page_template, body=template(form_template))

@application.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static/')

@application.post('/post')
def send():
    send_message(request.params)
    redirect(f'/thanks')

@application.route('/thanks')
def thanks():
    return template(page_template, body="""
    <h1>Thanks</h1>
    <a href="/">back</a>
    """)

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()