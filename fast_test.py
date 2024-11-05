import threading
from flask import Flask, render_template
import random
from turbo_flask import Turbo
from time import sleep

app = Flask(__name__)
turbo = Turbo(app)

@app.context_processor
def sensor():
    val = random.randint(1,20)
    return {'data': val}


def update_val():
    with app.app_context():
        while True:
            sleep(3)
            turbo.push(turbo.replace(render_template('zaza.html'), 'data'))


sched = BackgroundScheduler(daemon=True)
sched.add_job(update_val, 'interval', seconds=1)
sched.start()


@app.route("/")
def home():
    """ Function for test purposes. """
    return render_template('zaza.html')

if __name__ == "__main__":
    app.run()