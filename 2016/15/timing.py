def right_times():
    t = 0
    while True:
        if t % 17 == 1 and t % 3 ==2 and t % 19 == 12 \
          and t % 13 == 7 and t % 5 == 4 and t % 11 == 4:
            yield t
        t += 7

for t in right_times():
    print(t)
