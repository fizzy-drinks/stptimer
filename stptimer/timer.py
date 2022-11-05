from functools import reduce
import msvcrt
import os
from random import shuffle
import re
import time
from termcolor import colored, COLORS

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Char:
    LINEUP = '\033[F'

def kp(key: str):
    '''
    Get key press (non-blocking)

    TODO Unix support
    '''
    return msvcrt.kbhit() and key == msvcrt.getwch()

def wait_kp(keys: list[str]):
    '''
    Wait for key press and return character value

    TODO Unix support
    '''
    k = msvcrt.getwch().lower()
    return k if k in keys else wait_kp(keys)

def format_key(text: str):
    return colored(f'[{text}]', 'white', attrs=['bold'])

def print_turn_info(member: str):
    clear()
    print(f"{member}'s turn!")
    print(f"{format_key('Space')} start/stop  {format_key('N')}ext turn  {format_key('E')}xit\n")

def format_time(seconds: int):
    min = int(seconds // 60)
    sec = round(seconds % 60, 2)
    formatted = '{}\'{:0>5.2f}"'.format(min, sec)

    return formatted

def main():
    members: list[str] = []
    while True:
        m = input('Enter participant: ')
        if not m:
            break

        members.append(m)

    colors = list(COLORS.keys())
    shuffle(colors)

    members_pretty = list(colored(m, colors[i], attrs=['bold']) for i, m in enumerate(members))
    print('Turn order:', ', '.join(members_pretty))

    turn_time_seconds = int(input('Enter turn time in seconds: '))

    def time_color(seconds: int):
        color: str
        if seconds / turn_time_seconds < 0.5:
            color = 'cyan'
        elif seconds / turn_time_seconds < 0.75:
            color = 'white'
        elif seconds / turn_time_seconds < 1:
            color = 'yellow'
        else:
            color = 'red'

        return colored(format_time(seconds), color, attrs=['bold'])

    def print_report(member_times: list[int]):
        member_rows = (
            f'| {re.sub(m, p, m.ljust(9))} | {re.sub(format_time(t), time_color(t), format_time(t).rjust(9))} |'
            for m, p, t
            in zip(members, members_pretty, member_times)
            if t
        )

        print('''+-----------+-----------+
| Member    | Time      |
+-----------+-----------+
{}
+-----------+-----------+
| TOTAL     | {} |
+-----------+-----------+
'''.format(
            '\n'.join(member_rows),
            colored(format_time(reduce(lambda a, b: a + b, member_times)).rjust(9), 'white', attrs=['bold'])
        ))

    member_times: list[int] = []
    for member in members_pretty:
        print_turn_info(member)
        k = wait_kp([' ', 'n', 'e'])
        if 'n' == k:
            member_times.append(0)
            continue
        elif 'e' == k:
            print_report(member_times)
            exit(0)

        partial_member_time = 0
        start_time = time.time()
        while True:
            turn_time = round(time.time() - start_time, 2)
            print(f'{Char.LINEUP}{time_color(turn_time + partial_member_time)}')

            if kp(' '):
                k = wait_kp([' ', 'n', 'e'])
                if ' ' == k:
                    print_turn_info(member)

                    # Add current time to partial so we can acount for pauses
                    partial_member_time += turn_time
                    start_time = time.time()
                    continue
                elif 'n' == k:
                    member_times.append(turn_time + partial_member_time)
                    break
                elif 'e' == k:
                    member_times.append(turn_time + partial_member_time)
                    print_report(member_times)
                    exit(0)

    print_report(member_times)
