
import sys
from flask import Flask
from playbook import AlertBot

app = Flask(__name__)
config = sys.argv[1]

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