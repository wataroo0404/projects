
def reverse(expression):

    flip = ""
    i = 0
    expression = expression[::-1]
    startOfNumber = -1
    while i <= len(expression) - 1 :
        if ascii(expression[i]) >= ascii('0') and ascii(expression[i]) <= ascii('9'):
            if (startOfNumber == -1):
                startOfNumber = i
            flip = flip + expression[i]
        elif (len(flip) != 0):
            expression[startOfNumber:len(flip)] = flip
            startOfNumber = -1
        i = i + 1
              
    if (len(flip) != 0 ):
        expression[startOfNumber:len(flip)] = flip
    
    return expression