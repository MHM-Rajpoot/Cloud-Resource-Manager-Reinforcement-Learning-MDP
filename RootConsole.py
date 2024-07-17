
import os
import time
import pandas as pd 
from datetime import datetime

time_delay = int(5)

class RootSystem:

    def __init__(self) -> None:
        
        self.today = datetime.now().date()
        self.format_string = "%Y-%m-%d"
        self.totalvm = 9

    def dump_csv(self) -> None:
        # Dump data to CSV file
        self.data.to_csv('./Server/storage.csv', index=False)

    def load_csv(self) -> None:
        # Load CSV data and sort by rewards in descending order
        self.data  = pd.read_csv('./Server/storage.csv')
        self.data = self.data.sort_values(by='rewards', ascending=False)
        # Calculate available VMs based on reserved and online users
        self.avaliable = self.totalvm - (self.data[self.data['reseved'] == 1].shape[0] + self.data[self.data['online'] == 1].shape[0])

    def looping(self) -> None:
        # Main loop for managing system state

        self.load_csv()
        self.print_rotate_clock()

        self.reserve()
        self.unreserve()
        self.manage_reward()

        self.dump_csv()
        self.print_online_reserve_users()
   
    def reserve(self) -> None:
        # Reserve VMs for users with rewards
        reserved_rows = self.data[(self.data['time_difference'] >= -1 * (time_delay * 3)) & (self.data['time_difference'] <= (time_delay * 3))]
        reserved_rows = reserved_rows[(reserved_rows['reseved'] == 0) & (reserved_rows['online'] == 0) & (reserved_rows['rewards'] >= 1)]

        if not reserved_rows.empty and self.avaliable > 0:
            # Reserve VMs for users with rewards, up to a maximum of 8
            if len(reserved_rows) >= 8:
                reserved_rows = reserved_rows.head(8)

            print("\n Reserve: \n", reserved_rows, '\n')
            self.data.loc[reserved_rows.index, 'reseved'] = 1 
            self.avaliable = self.avaliable - len(reserved_rows)

        else:
            print("\n No records need reservation.")

    def unreserve(self) -> None:
        # Unreserve VMs for users who haven't used the system recently
        reserved_rows = self.data[(self.data['time_difference'] >= (time_delay * 5)) & (self.data['reseved'] == 1)]

        if not reserved_rows.empty:
            self.avaliable = len(reserved_rows)

            print("\n UnReserve: \n", reserved_rows, '\n')
            # Decrease rewards and unreserve VMs
            def update_reward(value):
                if value > 0:
                    return value - 1
                else:
                    return 0

            self.data.loc[reserved_rows.index, 'rewards'] = reserved_rows['rewards'].apply(update_reward)
            self.data.loc[reserved_rows.index, 'reseved'] = 0
            
            self.avaliable = self.avaliable + len(reserved_rows)

        else:
            print("\n No records need unreservation.")
    
    def manage_reward(self) -> None:
        # Manage rewards for users based on system usage
        
        for index, row in self.data.iterrows():
            if row['user_id'] != 0:
                last_day = datetime.strptime(str(row['day']), self.format_string).date()
                diff = self.today - last_day
                
                if (diff.days > 2) and row['rewards'] > 0:
                    # Decrease rewards if user hasn't used the system for more than 2 days
                    self.data.at[index, 'rewards'] -= diff.days
                    
                    if(row['rewards'] < 0):
                        self.data.at[index, 'rewards'] = 0
                    
                    self.data.at[index, 'day'] = self.today
                
                if (diff.days < 2) and row['reseved'] == 1 and row['online'] == 1:
                    # Unreserve VMs if user is online and reserved for more than 2 days
                    self.data.at[index, 'reseved'] = 0
                    self.data.at[index, 'rewards'] += 1
 
    def print_online_reserve_users(self) -> None:
        # Print information about online and reserved users
        
        for index, row in self.data.iterrows():
            if row['user_id'] != 0:
                if row['reseved'] == 1:
                    print('\n', row['user_id'], row['resource'], '\t Reservation')
                if row['online'] == 1:
                    print('\n', row['user_id'], row['resource'], '\t Online')

    def print_rotate_clock(self) ->None:
        # Print system clock and available VMs

        current_time = datetime.now().time()
        time_in_seconds = (current_time.hour * 3600) + (current_time.minute * 60) + current_time.second
        print('\n Clock :: ', time_in_seconds, ' Available VMs :: ', self.avaliable)

        for index, row in self.data.iterrows():
            if row['user_id'] != 0:
                self.data.at[index, 'time_difference'] = time_in_seconds - row['last_time']
            
# Create RootSystem object
obj = RootSystem()

while True:
    obj.looping()
    time.sleep(time_delay)
    os.system('cls')
