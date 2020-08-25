# -*- coding: utf-8 -*-
import os
from jinja2 import Template, Environment, PackageLoader, select_autoescape

# TODO: fix mailer module finder
# TODO: mailer sender
# TODO: restructure mailer
# TODO: send emails

package_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'webapp'))
env = Environment(
    loader=PackageLoader(os.getcwd()+"/webapp/", 'templates'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('mytemplate.html')

with open("email_list.txt", "r") as f:
    email_list: list = f.read().split_lines()

for email in email_list:
    html = template.render(unsubscribe_link_email=email)
