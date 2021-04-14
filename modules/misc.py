import os

from dnacentersdk import api
from ise import ERS


def get_dnac_access_devices():
    # DNAC instantiate, Settings located in environment variables
    dnac = api.DNACenterAPI()
    dnac.devices.get_device_list(role="ACCESS", family="Switches and Hubs")


def get_ise_devices():
    # ISE instantiate, settings located in environment variable
    ise = ERS(
        ise_node=os.environ["ISE_PAN"],
        ers_user=os.environ["ISE_ERS_ADMIN_USER"],
        ers_pass=os.environ["ISE_ERS_ADMIN_PASSWORD"],
        verify=False,
        disable_warnings=True,
    )

    # Declare dict for ISE device list
    isedevlist = {}
    # Declare list for ISE dict conversion to list
    isedevices = []

    # Check how many devices is in ISE so we can page through them with 100 items per page
    isecount = ise.get_devices(size=1)
    isetotaldevices = isecount["total"]
    pages = isetotaldevices // 100
    if isetotaldevices % 100 > 0:
        pages += 1

    # Iterate through ise pages and add to dict
    for page in range(1, pages + 1):
        # print(f'Fetch page:{page}')
        isedevlist.update(ise.get_devices(size=100, page=page)["response"])

    # Iterate thorugh ise device list dict, and get/print settings for each
    for isedevice in isedevlist:
        dev = ise.get_device(device=isedevice)["response"]

        # Catch keyerrors when some keys are not available, need to figure something simpler out.
        try:
            isedevices.append(dev)
        except KeyError:
            dev["trustsecsettings"]["deviceAuthenticationSettings"][
                "sgaDeviceId"
            ] = "NOT SET"
            dev["trustsecsettings"]["deviceAuthenticationSettings"][
                "sgaDevicePassword"
            ] = "NOT SET"
            isedevices.append(dev)

    return isedevices


# ndiff function comparing two strings
def diff_string(old, new):
    import difflib

    # Define text color, for different errors in ndiff result
    red = lambda text: f"\033[38;2;255;0;0m{text}\033[38;2;255;255;255m"
    green = lambda text: f"\033[38;2;0;255;0m{text}\033[38;2;255;255;255m"
    blue = lambda text: f"\033[38;2;0;0;255m{text}\033[38;2;255;255;255m"
    white = lambda text: f"\033[38;2;255;255;255m{text}\033[38;2;255;255;255m"
    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal":
            result += white(old[code[1] : code[2]])
        elif code[0] == "delete":
            result += red(old[code[1] : code[2]])
        elif code[0] == "insert":
            result += green(new[code[3] : code[4]])
        elif code[0] == "replace":
            result += red(old[code[1] : code[2]]) + green(new[code[3] : code[4]])
    return result


def check_compliance(dnac_devices, ise_devices):
    compliant = []
    noncompliant = []
    print(
        "Color code : RED = This part is missing in ISE, Green = This part is in ISE but not DNAC"
    )
    print(
        "Error            DNAC Host                              ISE Host                               DNACIP                     ISEIP                 DNAC SN             ISE CTSID "
    )
    for dnac_device in dnac_devices:
        for ise_device in ise_devices:
            if (
                dnac_device.managementIpAddress
                == ise_device["NetworkDeviceIPList"][0]["ipaddress"]
                and dnac_device.hostname == ise_device["name"]
                and dnac_device.serialNumber
                == ise_device["trustsecsettings"]["deviceAuthenticationSettings"][
                    "sgaDeviceId"
                ]
            ):
                compliant.append(dnac_device)
                break
        if (
            dnac_device.managementIpAddress
            == ise_device["NetworkDeviceIPList"][0]["ipaddress"]
            and dnac_device.serialNumber
            == ise_device["trustsecsettings"]["deviceAuthenticationSettings"][
                "sgaDeviceId"
            ]
            and not dnac_device.hostname == ise_device["name"]
        ):
            host_error = diff_string(dnac_device.hostname, ise_device["name"])
            print(
                f"Error hostname - DNAC:{host_error:30}    ISE:{ise_device['name']:30}     DNACIP:{dnac_device.managementIpAddress:15}     ISEIP:{ise_device['NetworkDeviceIPList'][0]['ipaddress']:15}"
            )
            noncompliant.append(dnac_device)
            break
        if (
            dnac_device.managementIpAddress
            == ise_device["NetworkDeviceIPList"][0]["ipaddress"]
            and dnac_device.hostname == ise_device["name"]
            and not dnac_device.serialNumber
            == ise_device["trustsecsettings"]["deviceAuthenticationSettings"][
                "sgaDeviceId"
            ]
        ):
            cts_error = diff_string(
                dnac_device.serialNumber,
                ise_device["trustsecsettings"]["deviceAuthenticationSettings"][
                    "sgaDeviceId"
                ],
            )
            print(
                f"Error cts      - DNAC:{dnac_device.hostname:30}    ISE:{ise_device['name']:30}     DNACIP:{dnac_device.managementIpAddress:15}     ISEIP:{ise_device['NetworkDeviceIPList'][0]['ipaddress']:15} DNAC SN:{cts_error} ISE CTSID:{ise_device['trustsecsettings']['deviceAuthenticationSettings']['sgaDeviceId']}"
            )
            noncompliant.append(dnac_device)
            break

    return compliant, noncompliant
