
import sys
import os.path
import yaml
import json
import mandrill
from flask import Flask




app = Flask(__name__)
config = sys.argv[1]


class AlertBot:

    def __init__(self, config, project, api_key, alert_id):
        self.set_config_file(config)
        self.project = project
        self.api_key = api_key
        self.alert_id = alert_id

    def set_config_file(self, config):
        if os.path.isfile(config):
            try:
                self.config = yaml.load(open(config).read())
            except:
                print '[ERROR] Failed to load definitions file'
                sys.exit(1)
        else:
            print '[ERROR] Definitions file does not exist'
            sys.exit(1)

    def get_config(self):
        return self.config

    def check_project(self):
        try:
            if str(self.api_key) == str(self.config[self.project]['api_key']):
                return True
        except Exception, e:
            print '[ERROR]', e
            return False

    def check_alert(self):
        alerts = self.config[self.project]['alerts']
        if str(self.alert_id) in alerts.keys():
            return True
        else:
            return False

    def do_action(self):
        alert = self.config[self.project]['alerts'][self.alert_id]
        if 'email' in alert.keys():
            print "---------------"
            self.send_email(alert['msg'], alert['email'], self.config[self.project]['mandrill'])
            return json.dumps(alert)

    def send_email(self, msg, email, mandrill_key):
        mandrill_client = mandrill.Mandrill(mandrill_key)
        print mandrill_client


@app.route('/alerts/<project>/<api_key>/<alert_id>')
def alerts(project, api_key, alert_id):

    bot = AlertBot(config, project, api_key, alert_id)

    if bot.check_project():
        if bot.check_alert():
            return bot.do_action()
        else:
            return "No alert found"
    else:
        return "Auth Failed"


app.run()
