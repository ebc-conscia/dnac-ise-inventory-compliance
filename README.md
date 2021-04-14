# Project name : DNAC ancd ISE Inventory Compliance Check (DIICC)

# Project summary :
Connects to a DNAC Instance and an ISE Deployment using API's, fetches and compares the NAD inventory of both, and shows the non-compliant entries, differences are only checked for hostname and cts id. DNAC inventory is treated as source of truth.

# Background 
DNAC does not cleanup the ISE NAD inventory when switches are deleted in DNAC, so inconsistencies can occur when the same switch is deployed a second time
and the IP or the name has changed. As there is still either the name or the ip from the previous deployment of the switch, DNAC fails to create or modify the existing switch in ISE, and radius, tacacs or trustsec may fail.

# Requirements, run before running the script itself
- `pip install -r requirements.txt`

# Running it
The script uses environment variables to get settings for the script, these must be set before running the script :

- DNA_CENTER_DEBUG=True (Print DNAC SDK debugs)
- DNA_CENTER_VERSION="1.3.3" (DNAC Version, only put three digit versions)
- DNA_CENTER_USERNAME="" (Admin role user in DNAC)
- DNA_CENTER_PASSWORD="" (Password)
- DNA_CENTER_BASE_URL="https://<fqdn or ip of DNAC VIP>" (Base url of DNAC)
- DNA_CENTER_VERIFY=False (Verify Root/Issuer chain of DNAC Cert)
- ISE_PAN="" (ISE Admin Node FQDN or IP)
- ISE_ERS_ADMIN_USER="" (ERS User with read rights to NAD list)
- ISE_ERS_ADMIN_PASSWORD="" (Password)

To load environment var, add your credentials and other details to environment.sh and use this to load it :
`source environment.sh`

Check vars are loaded with :
`export`

Script is run with below command, it will take a few minutes to complete so be patient :
`python3 run.py`

# Test
Tested on Python 3.8.2, but should work on anything 3.6 and above (f strings are used)

# Examples
The examples directory contains a few scripts that can be used as inspiration for further development of ISE, DNAC tools.
