current_mod_value = 1000000007


def get_answer():
    with open('input.txt') as file:
        first, second = [int(l) for l in file.readline().split()]
        WorkMatrix = [int(l) for l in file.readline().split()]
    WorkMatrix.sort()
    current_value = 1
    if second % 2:
        current_value *= WorkMatrix[-1]
        current_value %= current_mod_value
        second -= 1
        WorkMatrix.pop()
    if second > 1:
        left_index = 0
        right_index = 0
        if WorkMatrix[-1] > 0:
            while second > 1:
                second -= 2
                left = WorkMatrix[left_index] * WorkMatrix[left_index + 1]
                right = WorkMatrix[-1 - right_index] * WorkMatrix[-2 - right_index]
                if left > right:
                    current_value *= left
                    current_value %= current_mod_value
                    left_index += 2
                else:
                    current_value *= right
                    current_value %= current_mod_value
                    right_index += 2
        else:
            while second > 1:
                second -= 2
                current_value *= (WorkMatrix[-1 - right_index] * WorkMatrix[-2 - right_index])
                current_value %= current_mod_value
                right_index += 2
    print(current_value % current_mod_value)


if __name__ == "__main__":
    get_answer()
