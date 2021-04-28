# Project name: DNAC and ISE Inventory Compliance Check

# Project summary:
Connects to a DNAC Instance and an ISE Deployment using API's, fetches and compares the NAD inventory of both, and shows the non-compliant entries, differences are only checked for hostname and cts id. DNAC inventory is treated as source of truth.

# Background:
DNAC does not cleanup the ISE NAD inventory when switches are deleted in DNAC, so inconsistencies can occur when the same switch is deployed a second time
and the IP or the name has changed. As there is still either the name or the ip from the previous deployment of the switch, DNAC fails to create or modify the existing switch in ISE, and radius, tacacs or trustsec may fail.

# Relevant links:
[Learning Labs - Implementing Automation for Enterprise Solutions](https://learningnetworkstore.cisco.com/on-demand-e-learning/implementing-automation-for-cisco-enterprise-solutions-enaui-v1-2-elt-enaui-v1-024149 "Learning Labs - Automation for Enterprise")

[Sandbox - SDA + ISE](https://devnetsandbox.cisco.com/RM/Diagram/Index/b8d7aa34-aa8f-4bf2-9c42-302aaa2daafb?diagramType=Topology "Sandbox")
