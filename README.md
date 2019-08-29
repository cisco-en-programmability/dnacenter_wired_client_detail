# Cisco DNA Center Wired Client Detail


This Python script will retrieve information about a wired client using the Cisco DNA Center APIs.
This information is collected at the time the script is executed

**Cisco Products & Services:**

- Cisco DNA Center

**Tools & Frameworks:**

- Python environment

**Usage**

- $ python get_wired_client_info.py MAC_address

This script will use the Cisco DNA Center APIs to retrive information regarding wired clients.

Sample output:

Information for the client:
MAC Address:                  00:0C:29:CC:F0:62             
IPv4 Address:                 10.93.140.35                  
Access Switch:                NYC-9300                      
Switchport:                   GigabitEthernet1/0/1          
Access VLAN:                  123                           
Switchport State:             UP                            
Client Overall Healthscore:   10                            


This script may be changed to retrieve the information at a timestamp during the prior 7 days, or to add additional information about the client, as needed.

**License**

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
