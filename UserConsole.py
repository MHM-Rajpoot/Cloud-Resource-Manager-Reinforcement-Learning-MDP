
import os
import time
import pandas as pd 
from datetime import datetime
import atexit

class User:

    def __init__(self) -> None:
        # Initialize user attributes
        self.resource = []
        self.usage = [0, 0, 0, 0]
        self.max_res = [12, 32, 80, 80]
        self.default = [8, 16, 40, 40]

        self.action = [0, 0, 0, 0]
        self.timer = [0, 0, 0, 0]

    # Dump user data to CSV file
    def dump_csv(self) -> None:
        if 'time_difference' in self.data.columns:
            self.data = self.data.drop(columns=['time_difference'])
        self.data.to_csv('./Server/storage.csv', index=False)

    # Logout the user
    def logout(self) -> None:
        self.user_data.loc[self.data['user_id'] == self.id, 'online'] = 0
        self.data.loc[self.data['user_id'] == self.id, 'online'] = 0
        self.__init__()  # Reset user attributes
        self.dump_csv()

    # Concatenate resources and update user status to online
    def concat_res(self) -> None:
        res_str = ''.join(map(str, self.resource))
        res_str = "'0" + res_str + "'" if self.resource[0] < 10 else "'" + res_str + "'"
        self.user_data.loc[self.data['user_id'] == self.id, 'resource'] = res_str
        self.data.loc[self.data['user_id'] == self.id, 'resource'] = res_str
        self.data.loc[self.data['user_id'] == self.id, 'online'] = 1

    # Print user resource usage
    def print_user_usage(self) -> None:
        print(f'\n User ID :: {self.id} Timer :: {self.timer} \n')
        for i, resource_type in enumerate(['CPU', 'RAM', 'Storage', 'Network']):
            print(f' {resource_type} :: {self.usage[i]} of {self.resource[i]}')
        print()

    # Main loop for user interaction
    def looping(self, option, id) -> None:
        self.data = pd.read_csv('./Server/storage.csv')
        self.id = id

        if option == 1:
            self.login()
        elif option == 2:
            self.registration()
        else:
            return -1

    # Monitor and update current resource usage
    def current_usage_meter(self) -> None:
        while True:
            time.sleep(7)
            self.data = pd.read_csv('./Server/storage.csv')
            self.print_user_usage()
            print('\n LogOut 0 \n\n + Add - Subtract \n\n CPU 1 \n RAM 2 \n Storage 3 \n Network 4')

            choice = int(input('\n Enter Choice :: '))
            if choice == 0:
                self.logout()
                break
            for i in range(1, 5):
                if choice == i:
                    if self.resource[i - 1] > self.usage[i - 1]:
                        self.usage[i - 1] += 2 if i == 1 else 8 if i == 2 else 20
                elif choice == -i:
                    if self.usage[i - 1] > 0:
                        self.usage[i - 1] -= 2 if i == 1 else 8 if i == 2 else 20

            self.allocate()
            self.deallocate()
            self.concat_res()
            self.dump_csv()
            os.system('cls')

    # Login functionality
    def login(self) -> bool:
        self.user_data = self.data[self.data['user_id'] == self.id]

        if len(self.user_data) != int(1):
            print('\n No Such User Please Register')
            time.sleep(3)
            return 0

        temp = str(self.user_data['resource'].values[0])

        for i in range(1, 9, 2):
            self.resource.append(int(temp[i:i + 2]))

        datetime_now = datetime.now()
        date_today = datetime_now.date()
        current_time = datetime_now.time()
        time_in_seconds = (current_time.hour * 3600) + (current_time.minute * 60) + current_time.second

        self.user_data.loc[self.user_data['user_id'] == self.id, 'online'] = 1
        self.user_data.loc[self.user_data['user_id'] == self.id, 'day'] = date_today

        self.data.loc[self.data['user_id'] == self.id, 'online'] = 1
        self.data.loc[self.data['user_id'] == self.id, 'day'] = date_today

        self.dump_csv()
        self.current_usage_meter()

        return 1

    # Registration functionality
    def registration(self) -> None:
        max_id = self.data['user_id'].max() if not self.data.empty else 0
        self.id = max_id + 1
        self.user_data = self.data[self.data['user_id'] == 0]

        current_time = datetime.now().time()
        time_in_seconds = (current_time.hour * 3600) + (current_time.minute * 60) + current_time.second
        self.user_data.loc[self.user_data['last_time'] == 0, 'user_id'] = self.id
        self.user_data.loc[self.user_data['user_id'] == self.id, 'last_time'] = time_in_seconds

        self.data = pd.concat([self.data, self.user_data], ignore_index=True)
        self.login()

    # Allocate resources based on usage
    def allocate(self) -> None:
        for i in range(4):
            if self.usage[i] >= (0.8 * self.resource[i]):
                self.timer[i] += 1
                self.action[i] = 1

        for i in range(4):
            if self.timer[i] > 3:
                self.timer[i] = 0
                self.resource[i] += 2 if i == 0 else 8 if i == 1 else 20

    # Deallocate resources based on usage
    def deallocate(self) -> None:
        for i in range(4):
            if self.resource[i] > self.default[i]:
                self.timer[i] -= 1
            elif self.timer[i] > 0 and (self.action[i] == 0):
                self.timer[i] -= 1
            if self.timer[i] < -3:
                self.timer[i] = 0
                self.resource[i] -= 2 if i == 0 else 8 if i == 1 else 20

        self.action = [0, 0, 0, 0]

# Create user object
obj = User()
atexit.register(obj.logout)

while True:

    os.system('cls')
    print('\n Exit 0 \n LogIn 1  \n Registration 2')

    choice = int(input('\n Enter Choice :: '))
    if choice == 0:
        break
    elif choice == 1:
        user_id = int(input('\n Enter ID :: '))
        obj.looping(choice, user_id)
    else:
        obj.looping(choice, -1)