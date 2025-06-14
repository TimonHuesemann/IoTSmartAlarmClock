from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

alarm_times = {
    "Monday": "",
    "Tuesday": "",
    "Wednesday": "",
    "Thursday": "",
    "Friday": "",
    "Saturday": "",
    "Sunday": ""
}


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/set_alarm', methods=['GET', 'POST'])
def set_alarm():
    selected_day = ""  
    if request.method == 'POST':
        selected_day = request.form.get('day')
        alarm_time = request.form.get('alarm_time')
        if selected_day in alarm_times:
            alarm_times[selected_day] = alarm_time
    return render_template('set_alarm.html', days=alarm_times.keys(), alarm_times=alarm_times, selected_day=selected_day)




if __name__ == "__main__":
    app.run()