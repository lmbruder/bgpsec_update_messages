import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['savefig.dpi'] = 300

# bgp generation estimation
bgp = pd.read_csv('bgp.csv')
# bgp sec estimation based on prefix count without withdrawals
bgp_sec_without = pd.read_csv('bgpsec_without_withdrawals.csv')
# estimation for generated withdrawals
withdrawals = pd.read_csv('withdrawals.csv')

# format data
bgp['count'] = bgp['count'].astype(int)
bgp_sec_without['count'] = bgp_sec_without['count'].str.replace(',','').astype(int)
withdrawals['count'] = withdrawals['count'].astype(int)

# create new data frame for bgpsec estimation 
bgp_sec = pd.DataFrame({'time_block': [], 'count': []})
bgp_sec['time_block'] = bgp_sec_without['time_block']
# add bgp sec estimation based on prefix counts to estimated generated withdrawal messages
bgp_sec['count'] = bgp_sec_without['count'] + withdrawals['count']

# Plotting the data
plt.figure(figsize=(12, 6))
plt.bar(bgp_sec['time_block'], bgp_sec['count'], width=0.95, align='edge')
plt.bar(bgp['time_block'], bgp['count'], width=0.95, align='edge')
plt.xlabel('Time per 30 minutes', fontsize=18)
plt.ylabel('Count of update messages', fontsize=18)

plt.xlim(0, 48)

plt.xticks(rotation=45, ha='right')
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.legend(['With BGPsec (estimated)', 'Without BGPsec (estimated)'], prop={'size': 16}) 

# plt.show() 

# Save the plot
plt.savefig('estimation.png', format='png')