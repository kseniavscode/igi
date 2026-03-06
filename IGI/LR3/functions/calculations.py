def sum_F(x, n, eps) -> float:

    """
    Calculate the sum of the series ln(x+1).
    
    Args:
        x (float): argument in range [-1, 1]
        n (int): maximum number of iterations
        eps (float): precision
    
    Returns:
        float: calculated sum of the series
    """

    F = 0
    i = 1
    while True:
        part = (-1)**(i-1) * x**(i) / i
        F += part
        if abs(part) < eps or i == n:
            break 
        i += 1
    return F

def min_in_list(values: list) ->int:

    """
    Finding the min in values(list).
    
    Args:
        values(list): list of arguments without 1
    
    Returns:
        int: min
    """

    min = values[0]
    for i in range(1, len(values)):
        if values[i] < min:
            min = values[i]
    return min

def count_chars_in_low(string: str) ->int:

    """
    Finding elements of string in lower case.
    
    Args:
        string(str): inputting string
    
    Returns:
        int: count of chars in lower case
    """

    count = 0
    for i in range(len(string)):
        if(string[i].islower()):
            count += 1
    return count
def count_numbers(string: str) ->int:

    """
    Finding elements of string which are digits.
    
    Args:
        string(str): inputting string
    
    Returns:
        int: count of chars which are digits
    """

    count = 0
    for i in range(len(string)):
        if(string[i].isdigit()):
            count += 1
    return count