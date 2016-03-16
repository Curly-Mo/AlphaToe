import sys
import position
import alphatoe 


def parse_command(instruction, bot, pos):
    if instruction.startswith('action move'):
        time = int(instruction.split(' ')[-1])
        x, y = bot.get_move(pos, time)
        return 'place_move %d %d\n' % (x, y)
    elif instruction.startswith('update game field'):
        field_instruction = instruction.split(' ')[-1]
        pos.parse_field(field_instruction)
    elif instruction.startswith('update game macroboard'):
        macroboard_instruction = instruction.split(' ')[-1]
        pos.parse_macroboard(macroboard_instruction)
    elif instruction.startswith('update game move'):
        pos.nmove = int(instruction.split(' ')[-1])
    elif instruction.startswith('update game round'):
        pos.round = int(instruction.split(' ')[-1])
    elif instruction.startswith('settings player_names'):
        myname, oppname = instruction.split(' ')[-1].split(',')
        bot.myname = myname
        bot.oppname = oppname
    elif instruction.startswith('settings your_botid'):
        myid = int(instruction.split(' ')[-1])
        bot.myid = myid
        bot.oppid = 1 if myid == 2 else 2
    elif instruction.startswith('settings your_bot'):
        mybotname = instruction.split(' ')[-1]
        bot.mybotname = mybotname
    elif instruction.startswith('settings timebank'):
        bot.timebank = int(instruction.split(' ')[-1])
    elif instruction.startswith('settings time_per_move'):
        bot.time_per_move = int(instruction.split(' ')[-1])
    return ''


if __name__ == '__main__':
    pos = position.Position()
    bot = alphatoe.Bot()

    while True:
        try:
            instruction = raw_input()
        except Exception as e:
            sys.stderr.write(repr(e))
        out = parse_command(instruction, bot, pos)
        sys.stdout.write(out)
        sys.stdout.flush()
