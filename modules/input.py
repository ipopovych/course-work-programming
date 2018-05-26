def get_year():
    try:
        print('Please, choose one of the above options: ')
        print('1 - Get data on number of adjustificated judgements for one year\n'
              '2 - Get merged data on number of adjustificated judgements for several years\n')

        a = int(input('Enter the number: '))
        if a not in [1, 2]:
            raise ValueError('Invalid input')

    except ValueError:
        print('Invalid input')
        return get_year()
    else:
        return process_input(a)


def process_input(a):
    try:
        if a == 1:
            year = int(input('Please, enter the year to get data: '))
            return [year]
        elif a == 2:
            start = int(input('Please, enter the year to start with: '))
            end = int(input('Please, enter the last year to collect the data: '))
            return range(start, end+1)
    except ValueError:
        print('Invalid input')
        return process_input(a)


def specify(filters):
    try:
        n = int(input('Nice. Do you want to get information of ALL judjements (1) or give some specifications (2)? '))
        if n == 2:
            topics = [k for k in filters.keys()]
            print('Available specified topics: ' + '\n'.join(str(count+1)+'. '+str(el) for count, el in enumerate(topics)))
            topic = int(input('Select topic (enter number: '))
            return topics[topic-1]
        elif n == 1:
            return None
        else:
            print("Invalid input")
            return specify(filters)
    except ValueError:
        print("Invalid input")
        return specify(filters)
