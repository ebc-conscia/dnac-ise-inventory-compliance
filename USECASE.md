# Project name : DNAC and ISE Inventory Compliance Check (DIICC)

# Project summary :
Connects to a DNAC Instance and an ISE Deployment using API's, fetches and compares the NAD inventory of both, and shows the non-compliant entries, differences are only checked for hostname and cts id. DNAC inventory is treated as source of truth.

# Background 
DNAC does not cleanup the ISE NAD inventory when switches are deleted in DNAC, so inconsistencies can occur when the same switch is deployed a second time
and the IP or the name has changed. As there is still either the name or the ip from the previous deployment of the switch, DNAC fails to create or modify the existing switch in ISE, and radius, tacacs or trustsec may fail.
