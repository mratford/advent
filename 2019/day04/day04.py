def valid(number):
    double = False
    last_digit = 10

    # Go through the digits backwards
    while number > 0:
        number, next_digit = divmod(number, 10)
        if next_digit > last_digit:
            return False
        elif next_digit == last_digit:
            double = True
        last_digit = next_digit

    return double


def valid_2(number):
    double = False
    repeats = 0
    last_digit = 10
    
    # Go through the digits backwards
    while number > 0:
        number, next_digit = divmod(number, 10)
        if next_digit > last_digit:
            return False
        elif next_digit == last_digit:
            repeats += 1
        else:
            double = double or (repeats == 1)
            repeats = 0
            
        last_digit = next_digit

    return double or (repeats == 1)


if __name__ == '__main__':
    print('Part 1:', 
          len([x for x in range(272091, 815433) if valid(x)]))
    print('Part 2:', 
          len([x for x in range(272091, 815433) if valid_2(x)]))    