def add_to_five(number):
    """Returns ammount to be added to form a nearest 5"""
    return 5 - (number % 5)

def sub_to_five(number):
    """Returns ammount to be subtracted to form a nearest 5"""
    return number % 5

def efficient_change(payouts):
    """Calculate the most efficient ammounts of bank notes"""
    distribution = payouts.copy()
    change = {
        100:0,
        50:0,
        20:0,
        10:0,
        5:0,
        2:0,
        1:0
    }
    for person in distribution:
        while distribution[person] >= 100:
            change[100] += 1
            distribution[person] -= 100
        while distribution[person] >= 50:
            change[50] += 1
            distribution[person] -= 50
        while distribution[person] >= 20:
            change[20] += 1
            distribution[person] -= 20
        while distribution[person] >= 10:
            change[10] += 1
            distribution[person] -= 10
        while distribution[person] >= 5:
            change[5] += 1
            distribution[person] -= 5
        while distribution[person] >= 2:
            change[2] += 1
            distribution[person] -= 2
        while distribution[person] >= 1:
            change[1] += 1
            distribution[person] -= 1
    return change