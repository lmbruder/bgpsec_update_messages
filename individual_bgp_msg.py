import json
import os

# reformat json lines to include one bgp message per line
def reformat_bgp(json_file, ipv):
    # depending on ip version set field name
    if ipv == 4:
        nlri = 'bgp_bgp_nlri_prefix'
    elif ipv == 6:
        nlri = 'bgp_bgp_mp_reach_nlri_ipv6_prefix'

    bgp_documents = []
    filename = os.path.basename(json_file)
    with open(json_file, 'r') as file:
        for line in file:
            # load one frame
            packet = json.loads(line.strip())
            if "layers" in packet.keys():
                bgp_messages = packet['layers']['bgp']
                # if the value for key bgp is a list, separate bgp messages
                if isinstance(bgp_messages, list):
                    for bgp_message in bgp_messages:
                        prefix_count = 0
                        # if message contains NLRI field count prefixes
                        if nlri in bgp_message.keys():
                            if isinstance(bgp_message[nlri], str):
                                prefix_count = 1
                            else:
                                prefix_count = len(bgp_message[nlri])
                        # create new dictionary with single bgp message and prefix count
                        bgp_doc = {
                            'timestamp': packet['timestamp'],
                            'layers': {
                                'frame': {'filtered': 'frame'}, 
                                'eth': {'filtered': 'eth'}, 
                                'ip': {'filtered': 'ip'},   # or packet['layers']['ip'] if ip information is relevant
                                'tcp': {'filtered': 'tcp'}, 
                                'bgp': bgp_message,
                                'prefix_count': prefix_count
                            }            
                        }
                        bgp_documents.append(bgp_doc)

                else:
                    prefix_count = 0
                    # if message contains NLRI field count prefixes
                    if 'bgp_bgp_nlri_prefix' in packet['layers']['bgp'].keys():
                        if isinstance(packet['layers']['bgp'][nlri], str):
                            prefix_count = 1
                        else:
                            prefix_count = len(packet['layers']['bgp'][nlri])
                    packet['layers']['prefix_count'] = prefix_count
                    bgp_documents.append(packet)

    # specify results directory
    results_directory = '/path/to/folder/'
    with open(results_directory + 'mod_' + filename, 'w') as outfile:
        for doc in bgp_documents:
            outfile.write(json.dumps(doc) + '\n')

# directory with transformed pcaps
directory = '/path/to/folder/'
# specify ip version (4, 6)
ipv = 4
all_jsons = sorted(os.listdir(directory))
for json_file in all_jsons:
    print(json_file)
    reformat_bgp(directory + json_file, ipv)