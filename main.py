from typing import Tuple
import json
import datetime

from colorama import init

_hh = { 'h1': 6, 'h2': 11, 'h3': 16, 'h4': 21, 'h5': 26, 'h6': 31, 'h7': 36, 'h8': 41 }

def clear_screen():
    print("\033[2J")

def show_at(at: Tuple[int, int], toshow: str, hide: bool = True) -> None:
    x = int(at[1])
    if hide and len(toshow) >= 13:
        toshow = toshow[:8] + '...'
    if hide and len(toshow) > 5: x -= len(toshow) - 8
    print(f"\033[{at[0]};{x}H{toshow}\033[33B")

def draw_table():
    _table = None
    with open('empty_table.txt', 'r') as f:
        _table = f.readlines()
    print("".join(_table))

def read_json_data(_path: str):
    with open(f'./{_path}', 'r') as f:
        return json.load(f)['list']

def check_good_obj(_obj):
    for o in _obj:
        if not 'id' in o: return 'ID missing'
        if not 'alias' in o: return 'ALIAS missing'
        if not 'when' in o or type(o['when']) != list: return 'WHEN missing OR must be a list'
        for w in range(0, len(o['when'])):
            if not 'day' in o['when'][w]: return f'WHEN[{w}].DAY missing'
            assert o['when'][w]['day'] >= 1 and o['when'][w]['day'] <= 7, f"WHEN[{w}].DAY must be between 1 and 7"
            if not 'hour' in o['when'][w]: return f'WHEN[{w}].HOUR missing'
            assert str(o['when'][w]['hour']).startswith('h'), f"WHEN[{w}].HOUR format is `h[number of hour row];[number of row to add]`, ex: h5;2 -> h5 + h6"
    return 'Loaded data without any errors'

def get_position(_day, _hour: str):
    _start = None
    _end = None
    if ';' in _hour:
        _start = _hh[_hour.split(';')[0]]
        _end = _hh[f'h{int(_hour.split(";")[0][1]) + int(_hour.split(";")[1])}']
    else:
        _start = _hh[_hour[:2]]
        _end = _hh[f'h{int(_hour[1:2]) + 1}']
    return (18 + 16*(_day - 1), _start, _end)

def get_current_week_num():
    return datetime.datetime.now().isocalendar()[1]

def draw_colored_square():
    print("\033[41m")
    pos = get_position(1, 'h1')
    for i in range(1): show_at((pos[1] + i, pos[0]), ' ' * 13, False)
    print("\033[0m")

init()
clear_screen()
draw_table()
_data = read_json_data('plan1.jsonc')
print(check_good_obj(_data))
draw_colored_square()
for d in _data:
    dd = (d['id'], d['alias'])
    for h in d['when']:
        
        if 'parity' in h:
            if h['parity'] == 1 and get_current_week_num() % 2 != 1: continue
            if h['parity'] == 0 and get_current_week_num() % 2 != 0: continue
        pos = get_position(h['day'], h['hour'])
        show_at((pos[1] - 1, pos[0] - 1), '-' * 15, False)
        show_at((pos[1], pos[0]), dd[0])
        show_at((pos[1] + 1, pos[0] + 4), dd[1])
        show_at((pos[1] + 2, pos[0] + 8), h['type'])
        show_at((pos[2] - 1, pos[0] - 1), '-' * 15, False)