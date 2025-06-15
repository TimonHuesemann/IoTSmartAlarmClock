from flask import Flask, render_template, request, redirect, url_for


import Database.database_manager as db_manager

import time

RESET_DB = False

app = Flask(__name__)

db = db_manager.DatabaseManager()


def db_reset():
    """Reset the database by dropping existing tables and creating new ones."""
    db.connect()
    db.drop_table('alarms')
    db.drop_table('sleep_events')
    db.close()

if RESET_DB:
    db_reset() 


#set up the database
db.connect()




db.create_table('alarms', ['day TEXT PRIMARY KEY', 'time TEXT'])
db.create_table('sleep_events', ['timestamp TEXT', 'eventname TEXT'])


db.insert_data("sleep_events", (time.strftime("%Y-%m-%d %H:%M:%S"), "Tobias eliminated"))
db.close()



def set_alarm_in_db(day, time):
    """Set an alarm for a specific day and time."""
    print("Setting alarm for", day, "at", time)
    db.connect()
    db.insert_data('alarms', (day, time), replace=True)
    db.close()

def get_alarm(day):
    """Get the alarm time for a specific day."""
    db.connect()
    result = db.fetch_one("alarms", f"day = \"{day}\"")
    db.close()
    return result['time'] if result else None




@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/set_alarm', methods=['GET', 'POST'])
def set_alarm():
    selected_day = ""  
    
    alarm_dict = {day: get_alarm(day) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}

    if request.method == 'POST':
        selected_day = request.form.get('day')
        alarm_time = request.form.get('time')

        set_alarm_in_db(selected_day, alarm_time)

        alarm_dict = {day: get_alarm(day) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}

    return render_template('set_alarm.html', days=alarm_dict.keys(), alarm_times=alarm_dict, selected_day=selected_day)

@app.route('/reset_alarm/<day>', methods=['POST'])
def reset_alarm(day):
    db.connect()
    db.insert_data('alarms', (day, None), replace=True)
    db.close()
    return redirect(url_for('set_alarm'))




@app.route('/view_sleep_patterns', methods=['GET'])
def view_sleep_patterns():
    db.connect()
    sleep_events = db.fetch_all('sleep_events')
    db.close()
    return render_template('view_sleep_patterns.html', sleep_events=sleep_events)    




if __name__ == "__main__":
    app.run()