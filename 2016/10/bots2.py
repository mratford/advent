from collections import defaultdict


bot_chips = defaultdict(list)
bot_instructions = defaultdict(list)
outputs = defaultdict(list)
to_check = set()

with open('input', 'rt') as f:
    for fields in (l.strip().split() for l in f):
        if fields[0] == 'value':
            value = int(fields[1])
            bot = int(fields[5])
            bot_chips[bot].append(value)
            to_check.add(bot)
        else:  # bot code
            bot = int(fields[1])
            low_type = fields[5]
            low_id = int(fields[6])
            high_type = fields[10]
            high_id = int(fields[11])
            bot_instructions[bot] = ((low_type, low_id), (high_type, high_id))

while to_check:
    bot = to_check.pop()
    if len(bot_chips[bot]) == 2:
        # if 17 in bot_chips[bot] and 61 in bot_chips[bot]:
        #     print(bot)
        #     break
        low = min(bot_chips[bot])
        high = max(bot_chips[bot])
        if bot_instructions[bot][0][0] == 'bot':
            bot_chips[bot_instructions[bot][0][1]].append(low)
            to_check.add(bot_instructions[bot][0][1])
        else:
            outputs[bot_instructions[bot][0][1]].append(low)
        if bot_instructions[bot][1][0] == 'bot':
            bot_chips[bot_instructions[bot][1][1]].append(high)
            to_check.add(bot_instructions[bot][1][1])
        else:
            outputs[bot_instructions[bot][1][1]].append(high)
        bot_chips[bot] == []

print(outputs[0][0] * outputs[1][0] * outputs[2][0])
