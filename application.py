import os
from bottle import Bottle, run, template, route, redirect, static_file, request
from datetime import datetime
import boto3
from dotenv import load_dotenv

from nhs_html import *

load_dotenv()
application = Bottle()
client = boto3.client('sns', region_name='eu-west-2')

def page(**kwargs):
    return template('page', **kwargs)

questions = [
    html_text_input('email', 'What is your email address?'),
    html_text_input('role', 'What is your role?'),
    html_text_input('place_of_work', 'What is your place of work?'),
    html_text_area('challenge', 'Describe the challenge or problem (100 words max)',
        hint="e.g. GPs don't have full clarity on what over the counter medicines their patients are taking"),
    html_text_area('problem_impact', 'What impact does it have on patients and/or staff? (100 words max)',
        hint="e.g. Patients may be prescribed medications that interact with their over the counter medicines causing risks to their health."),
    html_text_area('current', 'What is currently being done to help ease this problem? (100 words max)',
        hint="e.g. GPs are having to spend considerable time repeatedly asking patients what over the counter medicines they have recently taken."),
    html_text_area('solution_impact', 'What would be the impact of solving this challenge? (100 words max)',
        hint="e.g. We could improve overall patient safety and reduce the risk of dangerous drug interactions."),
    html_conditional_radios('has_idea', 'Do you have an idea that could help solve this challenge?',
        html_text_area('idea', 'What is your idea?')),
    html_conditional_radios('has_been_tested', 'Has your idea has been tested before?',
        html_text_area('evidence', 'What evidence could you provide that your idea would help?')),
    html_checkboxes('focus_areas', 'Which of our focus areas does the problem apply to?',
        [{'value': 'burden', 'label': 'Reduce the burden on staff'},
         {'value': 'info', 'label': 'Help access clinical information'},
         {'value': 'productivity', 'label': 'Improve health and care productivity'},
         {'value': 'access', 'label': 'Provide tools to access services directly'},
         {'value': 'safety', 'label': 'Improve safety across health and care systems'}]),
    html_radios('involvement', 'If we pursue this problem, how involved would you like to be?',
        [{'value': 'not', 'label': 'I just want to submit a problem'},
         {'value': 'up_to_date', 'label': 'Keep me up to date on progress'},
         {'value': 'involve', 'label': "Involve me when I'm needed"},
         {'value': 'heavily', 'label': "I'd like to be heavily involved"}]),
    html_radios('can_test', 'If you work in a care setting, could we test any solutions with you?',
     [{'value': 'yes', 'label': 'Yes'},
      {'value': 'maybe', 'label': 'Maybe'},
      {'value': 'no', 'label': 'No'},
      {'value': 'not_care', 'label': "I don't work in a care setting"}])
]

html_questions = "\n".join([html_pad(question) for question in questions])

form_template=f"""
<h1>Submit a challenge or idea</h1>

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
    <a href="https://www.england.nhs.uk/privacy-policy/">data protection policy</a>.
    Please do not include any confidential or patient information.
  </p>

  {html_questions}
  {html_conditional_checkbox('consent', 'true',
    'Click here to agree',
    html_button('Submit'),
    hint='Your personal data will be stored in compliance with the <a href="https://www.england.nhs.uk/privacy-policy/">NHS England Privacy Policy</a>.  It will be used for the purposes of evaluating the information you send us, which may include contacting you in the future to discuss this challenge or other related challenges.  We may also invite you to anonymously provide feedback on your experience in order to improve this service. Please address any data protection requests to <a href="mailto:england.innovation.lab@nhs.net">england.innovation.lab@nhs.net</a>.')}
</form>
"""

def render_email(params):
    return template('email',
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
    return page(body=form_template)

@application.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static/')

@application.post('/post')
def send():
    send_message(request.params)
    redirect(f'/thanks')

@application.route('/thanks')
def thanks():
    return page(body=template('thanks'))

@application.route('/_dashboard')
def dashboard():
    return page(body=template('dashboard'))

@application.post('/smoke')
def smoke():
    isotime = datetime.now().isoformat()

    send_email(f"Front door delivery test email {isotime}",
    f"""
        This is a delivery test email.

        Sent at {isotime}.
    """)

    return page(body=template('dashboard_sent'))

def main():
    port = os.getenv('PORT', '3000')
    application.run(host="localhost", port=int(port))

if __name__ == "__main__":
    main()