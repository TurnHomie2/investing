import os




user_list = os.listdir('users')


real_estate_list = ['Small house', 'Apartment', 'Donut store', 'Phone factory', 'Aunt Belle\'s House']
investment_list = ['Bric Inc.', 'X-Phones']

for user in user_list:
    file = open(f'users/{user}/login_info.txt', 'r')
    login_info = {}

    for line in file:
        k, v = line.strip().split(':')
        login_info[k.strip()] = v.strip()
    file.close()

    for RE in real_estate_list:
        try:
            if login_info[f'{RE}_owned']:
                pass
        except:
            login_info[f'{RE}_owned'] = 'False'
            login_info[f'{RE}_mortgage'] = '0.0'
            login_info[f'{RE}_month_bought_on'] = 'None'

    for item in investment_list:
        try:
            if login_info[f'{item}_value']:
                pass
        except:
            login_info[f'{item}_value'] = '0.0'
            login_info[f'{item}_owned'] = '0'

    file = open(f'users/{user}/login_info.txt', 'w')
    for entry in login_info:
        file.write(f'{entry}:{login_info[entry]}\n')

    file.close()
