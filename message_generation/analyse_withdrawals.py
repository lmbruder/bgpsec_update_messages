import json
from jsondiff import diff
import os

class Analyse:
    def __init__(self):
        self.relevant_messages = []

    def find_duplicate_messages(self, file_path):
        '''
        gather information about message by storing first and last occurence
        {
            'bgp': item_bgp,
            'first_seen': timestamp,
            'last_seen': timestamp
        }
        '''
        # collect the time stamps when messages where first seen
        timestamp_list = []

        with open(file_path, 'r') as file:
            for line in file:
                packet = json.loads(line.strip())
                if 'bgp' in packet['layers'].keys():
                    timestamp = int(packet['timestamp'])
                    item_bgp = packet["layers"]["bgp"]

                    # remove all old messages and add timestamps to list
                    self.relevant_messages = [x for x in self.relevant_messages if not timestamp_check(timestamp, x.get('last_seen')) or timestamp_list.append(x.get('first_seen'))]

                    # if not UPDATE message and not withdrawal message; skip!
                    if item_bgp.get('bgp_bgp_type') == "2" and packet['layers'].get('prefix_count') == 0:
                        message_found = 0
                        # go through all messages
                        for message in self.relevant_messages:
                            if message.get('bgp') == item_bgp:
                                message_found = 1

                                message['last_seen'] = timestamp

                        if not message_found:
                            # if message is not in the list yet, add it
                            new_item = {
                                'bgp': item_bgp,
                                'first_seen': timestamp,
                                'last_seen': timestamp
                                }
                            self.relevant_messages.append(new_item)

        file_name = os.path.basename(file_path) 
        results_directory = '/path/to/folder/'
        with open(f'{results_directory}timestamp_list_withdrawals_{file_name}.csv', 'w') as output:
            output.write("timestamp\n")
            for item in timestamp_list:
                output.write(f"{item}\n")

def timestamp_check(timestamp, last_seen):
    return timestamp - last_seen > 100


run = Analyse()
directory = '/path/to/folder/'
all_files = sorted(os.listdir(directory))
for data in all_files:
    print(data)
    run.find_duplicate_messages(directory + data)
