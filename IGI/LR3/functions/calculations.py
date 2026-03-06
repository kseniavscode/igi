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