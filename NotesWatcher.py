import json
import copy

map_path = r"C:\Program Files (x86)\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels\21f6 (quaver - hexagonial)\ExpertPlus.dat"
info_path = r"C:\Program Files (x86)\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels\21f6 (quaver - hexagonial)\info.dat"

data = json.load(open(map_path, 'rb'))
info = json.load(open(info_path, 'rb'))

bpm = float(info['_beatsPerMinute'])
print('bpm is', bpm)

all_events = data['_notes']


def make_notes(all_events, event_type):
    ans = []
    last_time = 0
    for a in all_events:
        if a['_type'] == event_type:
            now_time = a['_time']
            grid = now_time - last_time
            if grid < 0.99:
                continue
            ans.append(a)
            last_time = now_time
    return ans


def make_json(notes_data):
    notes_num = len(notes_data)
    notes_info = []

    for i in range(notes_num):

        if i < 10:
            print(notes_data[i])
        if i == 0:
            duration = notes_data[0]['_time'] - 1
            W_Pos = 1.5

            H_Pos = 1.0
            notes_info.append((duration, W_Pos, H_Pos))
            continue
        duration = (notes_data[i]['_time'] - notes_data[i - 1]['_time'])
        W_Pos = notes_data[i - 1]['_lineIndex']  #from_left_to_middle
        H_Pos = notes_data[i - 1]['_lineLayer']  #from_bottom_to_top

        notes_info.append((duration, W_Pos, H_Pos))

    for i in range(notes_num):
        if i < 10:
            print(notes_info[i])

    def Camera_Pos(w, h):
        x = w - 1.5
        x = x / 1.5
        y = h - 0.5
        y = 1 + y / 2
        return x, y

    j = json.load(open('template.json', 'rb'))

    for i in range(notes_num):
        new_j = copy.deepcopy(j["Movements"][0])
        new_j['Duration'] = notes_info[i][0] * 60 / bpm
        x, y = Camera_Pos(notes_info[i][1], notes_info[i][2])
        new_j['StartPos']['x'] = x
        new_j['StartPos']['y'] = y
        new_j['StartPos']['z'] = -2.5
        new_j['EndPos']['x'] = x
        new_j['EndPos']['y'] = y
        new_j['EndPos']['z'] = -2.5
        j['Movements'].append(new_j)

    for i in range(notes_num):
        if i < 10:
            print(j['Movements'][i])

    return j


blue_notes = make_notes(all_events, 1)
blue_json = make_json(blue_notes)
target_path = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Beat Saber\\UserData\\CameraPlus\\Scripts\\NotesWatcher_Blue.json'
json.dump(blue_json, open(target_path, 'w'), indent=4)

red_notes = make_notes(all_events, 0)
red_json = make_json(red_notes)
target_path = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Beat Saber\\UserData\\CameraPlus\\Scripts\\NotesWatcher_Red.json'
json.dump(red_json, open(target_path, 'w'), indent=4)
