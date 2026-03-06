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

def split_string(string:str):
    """
    Split string -> list
    
    Args:
        string(str): string
    
    Returns:
        list: words
    """
    str_new = string.replace(',', ' ')
    str_new_2 = str_new.replace('.', ' ')

    parts = []
    for i in str_new_2.split(' '):
        if i.strip():
            parts.append(i.strip())
    return parts
def count_odd_num_of_letters(parts:list) ->list:

    """
    Finding elements of list with an odd number of letters .
    
    Args:
        parts(list): list of words
    
    Returns:
        list: words + count of chars with an odd number of letters
    """

    count = 0
    odd_parts = []
    for part in parts:
        if len(part) % 2 == 1:
            count += 1
            odd_parts.append(part)
    odd_parts.append(count)
    return odd_parts


def shortest_started_i(l:list):

    """
    Finding elements of string started with i .
    
    Args:
        l(list): list of words
    
    Returns:
        a word started with i or n, if not found 
    """
     
    start_i = []
    for i in l[:-1]:
        if i[0].lower() == 'i':
            start_i.append(i)
    if len(start_i) == 0:
        return 'n'
    short = start_i[0]
    for j in start_i[1:]:
        if len(j) < len(short):
            short = start_i[j]
    return short