import functools


data = open('input', 'r').read().strip()

# Part 1

layers = [data[i:i+150] for i in range(0, len(data), 150)]
fewest_zeroes = min(layers, key=lambda xs: xs.count('0'))
print(fewest_zeroes.count('1') * fewest_zeroes.count('2'))


# Part 2

def first_non_two(xs):
    try:
        return next(x for x in xs if x != '2')
    except:
        return '2'

pixels = [first_non_two(pixel_layers)
          for pixel_layers in zip(*layers)]
for i in range(0, len(pixels), 25):
    print(''.join(pixels[i:i+25]).replace('0', ' ').replace('1', '#'))
