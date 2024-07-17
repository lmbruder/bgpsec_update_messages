## Analysis of the impact of BGPsec on the amount of generated BGP update messages

This repository contains commands and python scripts that I used while researching BGPsec update messages for my 6-week Master thesis at the University of Amsterdam.
This project was supervised by Ralph Koning (UvA/SIDN Labs) and Moritz Müller (UT/SIDN Labs).


### Abstract from the report
*This report analyses the impact of BGPsec on BGP update messages. BGPsec is an extension to traditional BGP that aims to improve routing security by allowing BGP 
speakers to sign and validate AS paths. We make use of BGP data streams from two BGP speakers and evaluate how different identified types of BGP update messages 
are affected by the changes required by BGPsec. In addition to the lack of support for update packing, these changes include the need to tailor each update message 
to the receiving peer by adding its AS number to the path. We model BGPsec traffic based on these requirements. We analyse the impact of BGPsec on the generation of 
update messages and conclude that the increased number of messages is likely to significantly increase the computational load on routers running BGP, even without 
considering the computational cost of signing. However, we find that the average number of prefixes advertised per update message is lower than the ones determined 
in previous work, which may indicate a lower than expected impact of BGPsec on BGP traffic.*

### Overview of workflow
<img src="https://github.com/lmbruder/bgpsec_update_messages/blob/main/workflow.png" width=85%/>

### Filter and transform
Transform and filter all pcaps in a folder.

#### IPv4:
```
for f in *; do tshark -2 -R "ip.src==<ipv4-src-ip> and bgp.type==2" -r "$f" -T ek -J "bgp ip" > "$f".json; echo "$f"; done
```

#### IPv6:
```
for f in *; do tshark -2 -R "ipv6.src==<ipv6-src-ip> and bgp.type==2" -r "$f" -T ek -J "bgp ipv6" > "$f".json; echo "$f"; done
```

### Split up packets and count prefixes
Several BGP messages included in one frame can be separated using the ``individual_bgp_msg.py`` script.


### Elasticsearch and Kibana
The prepared JSON lines files can be imported to Elasticsearch with for example logstash. An example pipeline configuration can be found in the ELK folder (``logstash_example.conf``).

This folder also includes a Kibana dashboard to easily start analysing and visualising the imported data. It can be imported into Kibana through Stack Management > Saved Objects > Import. 


### Message generation analysis
The ``message_generation`` contains several python scripts to analyse message generation with BGPsec compared to BGP.

The scripts ``analyse.py`` and ``analyse_withdrawals.py`` can be used to determine the count of generated update messages and the count of generated withdrawal messages. These scripts output files that contain timestamps at which messages were created.
Based on that the ``prepare_for_plot.py`` script can be used to reformat them to a CSV that contains timestamps at the count of messages in the chosen time frames.
Finally, the ``plot.py`` script can be used to visualise the result.

