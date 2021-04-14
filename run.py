from modules import check_compliance, get_dnac_access_devices, get_ise_devices

dnacdevices = get_dnac_access_devices()
isedevices = get_ise_devices()

# the check_compliance function returns two lists, but also prints status to screen.
compliant, noncompliant = check_compliance(dnacdevices, isedevices)
