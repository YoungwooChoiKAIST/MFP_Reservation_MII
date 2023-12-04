from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

app.config['calendar'] = {
    "MON 07":0,
    "MON 13":0,
    "MON 19":0,
    "TUE 07":0,
    "TUE 13":0,
    "TUE 19":0,
    "WED 07":0,
    "WED 13":0,
    "WED 19":0,
    "THR 07":0,
    "THR 13":0,
    "THR 19":0,
    "FRI 07":0,
    "FRI 13":0,
    "FRI 19":0,
    "SAT 07":0,
    "SAT 13":0,
    "SAT 19":0,
    "SUN 07":0,
    "SUN 13":0,
    "SUN 19":0,
}

# 전체 일정을 저장할 리스트
all_schedules = []

@app.route('/')
def index():
    return render_template('index.html', calendar=app.config['calendar'], all_schedules=all_schedules)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    schedule = request.form.get('schedule')
    count = int(request.form.get('count'))
    
    schedule_list = schedule.split(',')
    schedule_list = [x.strip() for x in schedule_list]
    
    # 각 일정에 ID 부여
    schedule_id = len(all_schedules) + 1

    # 받은 일정을 전체 일정 리스트에 추가
    all_schedules.append({
        "id": schedule_id,
        "name": name,
        "schedule": schedule_list,
        "count": count
    })

    return render_template('index.html', calendar=app.config['calendar'], all_schedules=all_schedules)

@app.route('/edit/<int:schedule_id>', methods=['GET', 'POST'])
def edit(schedule_id):
    if request.method == 'GET':
        # 해당 ID에 해당하는 일정 정보를 가져옴
        schedule = next((schedule for schedule in all_schedules if schedule['id'] == schedule_id), None)
        return render_template('edit.html', calendar=app.config['calendar'], schedule=schedule)
    elif request.method == 'POST':
        # 해당 ID에 해당하는 일정 정보를 수정
        schedule = next((schedule for schedule in all_schedules if schedule['id'] == schedule_id), None)
        if schedule:
            name = request.form.get('name')
            schedule_str = request.form.get('schedule')
            count = int(request.form.get('count'))
            schedule_list = schedule_str.split(',')
            schedule_list = [x.strip() for x in schedule_list]

            schedule['name'] = name
            schedule['schedule'] = schedule_list
            schedule['count'] = count

    return redirect('/')

@app.route('/delete/<int:schedule_id>', methods=['GET'])
def delete(schedule_id):
    # 해당 ID에 해당하는 일정 정보를 삭제
    global all_schedules
    all_schedules = [schedule for schedule in all_schedules if schedule['id'] != schedule_id]
    return redirect('/')

@app.route('/delete_all', methods=['GET'])
def delete_all():
    global all_schedules
    all_schedules = []
    return redirect('/')

@app.route('/reset_all', methods=['GET'])
def reset_all():
    for key in app.config['calendar'].keys():
        app.config['calendar'][key]=0
    return redirect('/')

@app.route('/finalize', methods=['GET'])
def finalize_schedule():
    finalize_schedules(all_schedules)
    return redirect('/')

def finalize_schedules(schedules):
    random.shuffle(schedules)
    while not all(user["count"] <= 0 for user in schedules):
        make_reservation(schedules)
    delete_all()

# 해당 시간대가 이미 예약되었는지 확인하는 함수
def is_time_slot_reserved(time_slot):
    # 여기에서 예약 상태를 확인하고 반환합니다.
    # 예: 이미 예약된 시간이라면 True를 반환하고, 아니면 False를 반환합니다.
    if app.config['calendar'][time_slot]==0:
        return False
    return True

# 해당 시간대를 예약하는 함수
def reserve_time_slot(time_slot, user):
    # 여기에서 예약을 진행하고 예약 상태를 업데이트합니다.
    # 예약에 성공한 경우 True를 반환하고, 실패한 경우 False를 반환합니다.
    app.config['calendar'][time_slot]=user['name']
    return True

def make_reservation(schedules):
    for schedule in schedules + schedules[::-1]:
        if schedule["count"] <= 0:
            continue  # 이미 모든 일정을 예약한 사용자는 건너뜁니다
        reservable = False
        for time_slot in schedule["schedule"]:
            if not is_time_slot_reserved(time_slot):
                reservable = True
                reserve_time_slot(time_slot, schedule)
                schedule["count"] -= 1
                break
        if not reservable:
            schedule["count"] = 0
        if schedule["count"] == 0:
            pass

if __name__ == '__main__':
    app.run(debug=True)
