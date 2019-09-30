'''
Parses Fastest Path String given from Algorithm. Returns a sequence
of steps which Android can consume immediately
Input Examples:
    singleStepData = "FP|(10,10,N);(10,11,N);(10,12,N);(11,12,E)"
    multiStepData = "FP|(10,10,N);(10,12,N);(11,12,E)"
Output Examples:
    ['F', 'F', 'TR', 'F']
'''
def fpParser(path_data):
    hori = ['E', 'W']
    vert = ['N', 'S']
    step_seq = []

    path_seq = path_data.split(";")
    init_x, init_y, init_direction = path_seq[0][slice(1, len(path_seq[0]) - 1)].split(',')
    print(init_x, init_y, init_direction)

    for index, path in enumerate(path_seq):
        x_1, y_1, direction_1 = path[slice(1, len(path) - 1)].split(',')

        if (index + 1) == len(path_seq):
          break
        else:
            x_2, y_2, direction_2 = path_seq[index + 1][slice(1, len(path) - 1)].split(',')
            
            if direction_1 == direction_2:
                if direction_1 in vert:
                    step_count = abs(int(y_1) - int(y_2))
                elif direction_1 in hori:
                    step_count = abs(int(x_1) - int(x_2))
                step_seq = step_seq + [ 'f' for x in range(step_count) ]
            else:
                if (direction_1 == 'N' and direction_2 =='E')\
                    or (direction_1 == 'S' and direction_2 == 'W')\
                    or (direction_1 == 'E' and direction_2 == 'S')\
                    or (direction_1 == 'W' and direction_2 == 'N'):
                    step_seq.append('tr')
                elif (direction_1 == 'N' and direction_2 =='W')\
                    or (direction_1 == 'S' and direction_2 == 'E')\
                    or (direction_1 == 'E' and direction_2 == 'N')\
                    or (direction_1 == 'W' and direction_2 == 'S'):
                    step_seq.append('tl')

                if direction_2 in vert:
                    step_count = abs(int(y_1) - int(y_2))
                elif direction_2 in hori:
                    step_count = abs(int(x_1) - int(x_2))
                step_seq = step_seq + [ 'f' for x in range(step_count) ]

    return 'FP|{x}|{y}|{d}|{steps}'.format(x=init_x, y=init_y, d=init_direction, steps=','.join(step_seq))