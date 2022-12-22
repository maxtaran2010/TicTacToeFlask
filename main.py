import random
import string

from flask import Flask, render_template, request, redirect


app = Flask(__name__)
rooms = {}
winner = ''


def all_lines(world):
    line1 = world[0]
    line2 = world[1]
    line3 = world[2]
    line4 = [world[0][1], world[1][1], world[2][1]]
    line5 = [world[0][0], world[1][0], world[2][0]]
    line6 = [world[0][2], world[1][2], world[2][2]]
    line7 = [world[0][0], world[1][1], world[2][2]]
    line8 = [world[0][2], world[1][1], world[2][0]]
    return [line1, line2, line3, line4, line5, line6, line7, line8]


def all_same(m):
    val = m[0]
    for i in m:
        if i != val:
            return False
    return val


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/game')
def login():
    code = request.args['code']
    name = request.args['name']
    value = request.args['value']
    room = rooms.get(code, None)
    if room is None:
        return '<h1> no such room. </h1><a href="/">General</a>'
    if winner:
        return "game end! Winner: "+winner
    if name not in room['users']:
        room['users'].append(name)
    if len(room['users']) > 2:
        room['users'].pop(-1)
        return '<h1> This room is full </h1><a href="/">General</a>' + str(len(room['users']))+str(room['users'])
    return render_template('game.html', code=code, room=room, name=name, value=value)


@app.route('/click')
def click():
    global winner
    value = request.args['value']
    room = rooms[request.args['code']]
    name = request.args['name']
    pos = list(map(int, request.args['pos'].split('|')))
    if room['world'][pos[0]][pos[1]] == "" and room['step'] == value:
        room['world'][pos[0]][pos[1]] = value
        room['step'] = 'o' if room['step'] == 'x' else 'x'
    for i in all_lines(room['world']):
        if all_same(i):
            winner = all_same(i)

    return redirect(f'/game?code={request.args["code"]}&name={name}&value={value}')


@app.route('/create')
def create():
    name = request.args['name']
    code = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)])
    rooms.update({code: {"users": [], "world": [['', '', ''], ['', '', ''], ['', '', '']], 'step': 'x'}})
    return redirect(f'/game?name={name}&code={code}&value=x')


@app.route('/clear')
def clear():
    code = request.args['code']
    room = rooms[code]
    name = request.args['name']
    value = request.args['value']
    room['world'] = [['', '', ''], ['', '', ''], ['', '', '']]
    room['step'] = 'x'
    return redirect(f'/game?code={code}&name={name}&value={value}')


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
