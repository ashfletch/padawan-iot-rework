import subprocess
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")
def homepage():
    return render_template("home.html")


@app.route('/shutdown', methods=['POST', 'GET'])
def shutdown():
    return render_template("shutdown.html")


@app.route('/confirmshutdown', methods=['POST'])
def confirmshutdown():
    """Form submission confirmation from shutdown page."""
    shutdown_type = request.form.get('shutdownType')
    if shutdown_type == 'shutdown':
        subprocess.run('sudo shutdown -P 1', shell=True)
    elif shutdown_type == 'reboot':
        subprocess.run('sudo shutdown -r 1 ', shell=True)
    else:
        return redirect(url_for('home'))
    return redirect(url_for('shutdown'))


@app.route("/metrics")
def metrics():
    return render_template("metrics.html")


@app.route("/logs")
def logs():
    return render_template("logs.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
