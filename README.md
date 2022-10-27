Innovation Lab Front Door Form
==============================

ABOUT
-----

This is a simple form to gather information from clinical and non-clinical staff about challenges and opportunities where we might apply innovative techniques and technologies.  It has no storage: it sends the information as an email to a designated email address.

It uses AWS services, and is intended to be run in Elastic Beanstalk.  Email sending is via an AWS SNS subscription.

USAGE
-----

It runs on Python 3.9 locally, but there is nothing preventing earlier versions.

To test fully locally, you will need to set a `FRONTDOOR_SNS_ARN` environment variable with the ARN of a queue in SNS.  You will need to configure the eventual destination email address as a subscription to that topic, create a policy with the `sns:Publish` privilege on that topic, and grant that policy to the built-in `aws-elasticbeanstalk-ec2-role` role (or another you create and assign to the application).

With the correct python installed, install dependencies like so:

````
$ make deps
````

Run the server with:

````
$ make up
````

If you need to run the server on a port other than the default `3000`, you can specify a `PORT` environment variable:

````
$ PORT=8080 make up
````

When running, the form will be available at http://localhost:3000/.  There is also a dashboard at http://localhost:3000/_dashboard which has a button to send a delivery test email.

CONTRIBUTING
------------

Open an issue or a PR to contribute.  If you want to check in before doing so, see AUTHOR below.

AUTHOR
------

Alex Young <alex.young12@nhs.net>
NHSE Innovation Lab <england.innovation.lab@nhs.net>