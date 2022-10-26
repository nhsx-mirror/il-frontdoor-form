import os
from bottle import Bottle, run, template, route, redirect, static_file, request
from datetime import datetime
import boto3
from random import randint
from dotenv import load_dotenv

load_dotenv()
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
        <input class="nhsuk-checkboxes__input" id="{name}-{value}" name="{name}" type="checkbox" value="{value}">
        <label class="nhsuk-label nhsuk-checkboxes__label" for="{name}-{value}">
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

def html_button(value):
    return f"""
        <div class="nhsuk-form-group">
            <input type="submit" class="nhsuk-button" value="{value}">
        </div>
    """

def html_conditional_checkbox(name, checkbox_value, checkbox_label, conditional_content, hint=None):
    html_hint = f"""
      <div class="nhsuk-hint" id="{name}-hint">
        {hint}
      </div>
    """ if hint else ''

    return f"""
    {html_hint}
    <div class="nhsuk-checkboxes nhsuk-checkboxes--conditional">
        <div class="nhsuk-checkboxes__item">
          <input class="nhsuk-checkboxes__input" id="{name}" name="{name}" type="checkbox" value="{checkbox_value}" aria-controls="conditional-{name}" aria-expanded="false">
          <label class="nhsuk-label nhsuk-checkboxes__label" for="{name}">
            {checkbox_label}
          </label>
        </div>

        <div class="nhsuk-checkboxes__conditional nhsuk-checkboxes__conditional--hidden" id="conditional-{name}">
            {conditional_content}
        </div>
    </div>
"""

def page(**kwargs):
    return template('page', **kwargs)

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
    We don't take submissions relating to existing solutions or products.
    Please see our
    <a href="https://transform.england.nhs.uk/innovation-lab/send-us-your-challenges/">guidance</a>
    on what challenges are suitable.
  </p>

  <p>
    All submissions will be handled in accordance with our
    <a href="https://transform.england.nhs.uk/privacy-policy/">data protection policy</a>.
    Please do not include any confidential or patient information.
  </p>

  {html_text_input('email', 'What is your email address?')}
  {html_text_input('role', 'What is your role?')}
  {html_text_input('place_of_work', 'What is your place of work?')}
  {html_text_area('challenge', 'In 100 words or less, describe the challenge.')}
  {html_text_area('problem_impact', 'In 100 words or less, describe the impact on patients and/or staff.')}
  {html_text_area('current', 'In 100 words or less, describe what is currently being done to help ease this problem.')}
  {html_text_area('solution_impact', 'In 100 words or less, describe the impact of solving this challenge.')}
  {html_conditional_checkbox('has_idea', 'true', 'Click if you have an idea that could help solve this challenge.',
    html_text_area('idea', 'What is your idea?'))}
  {html_conditional_checkbox('has_been_tested', 'true', 'Click if your idea has been tested before.',
    html_text_area('evidence', 'What evidence could you provide that your idea would help?'))}
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
  {html_conditional_checkbox('consent', 'true',
    'Click here to agree',
    html_button('Submit'),
    hint='Your personal data will be stored in compliance with the NHSX Privacy Policy.  It will be used for the purposes of evaluating the information you send us, which may include contacting you in the future to discuss this challenge or other related challenges.  We may also invite you to anonymously provide feedback on your experience in order to improve this service. Please address any data protection requests to <a href="mailto:innovation-lab@nhsx.nhs.uk">innovation-lab@nhsx.nhs.uk</a>.')}
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

In 100 words or less, describe the impact on patients and/or staff.
-------------------------------------------------------------------
{{problem_impact}}

In 100 words or less, describe what is currently being done to help ease this problem.
--------------------------------------------------------------------------------------
{{current}}

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
      problem_impact=params.get('problem_impact'),
      current=params.get('current'),
      solution_impact=params.get('solution_impact'),
      has_idea='Yes' if params.get('has_idea') == 'true' else 'No',
      idea=params.get('idea'),
      has_been_tested='Yes' if params.get('has_been_tested') == 'true' else 'No',
      evidence=params.get('evidence'),
      focus_areas=", ".join(params.getall('focus_areas')),
      involvement=params.get('involvement'),
      can_test=params.get('can_test'))

def send_email(subj, msg):
    response = client.publish(
        TopicArn=os.getenv('FRONTDOOR_SNS_ARN'),
        Message=msg,
        Subject=subj
    )
    print(response)

def send_message(params):
    isotime = datetime.now().isoformat()
    subj = f"Front door submission at {isotime}"
    msg = render_email(request.params)
    send_email(subj, msg)

@application.route('/')
def index():
    return page(body=template(form_template))

@application.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static/')

@application.post('/post')
def send():
    send_message(request.params)
    redirect(f'/thanks')

@application.route('/thanks')
def thanks():
    return page(body="""
    <h1>Thank you!</h1>

    <p>
        Thank you for your input.  We appreciate the effort you've gone to in making us aware of your challenge.
    </p>

    <p>
        If you indicated that you wanted to be involved, we will get in touch about our next steps.
        Please don't hesitate to send us more challenges when you find them.
    </p>
    """)

@application.route('/_dashboard')
def dashboard():
    return page(body="""
    <h1>Service Dashboard</h1>

    <form action="/smoke" method="post">
      <input type="submit" class="nhsuk-button" value="Delivery test"/>
    </form>
    """)

@application.post('/smoke')
def smoke():
    isotime = datetime.now().isoformat()

    send_email(f"Front door delivery test email {isotime}",
    f"""
        This is a delivery test email.

        Sent at {isotime}.
    """)

    return page(body=f"""
    <p>
        Delivery test message sent at {isotime}.
    </p>

    <form action="/smoke" method="post">
      <input type="submit" class="nhsuk-button" value="Send another"/>
    </form>
    """)

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()