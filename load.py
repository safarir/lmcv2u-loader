import usb.core
import usb.util
import struct
import hashlib

VENDOR_ID = 0x9588
PRODUCT_ID = 0x9980
KNOWN_HASH = "b86bc139a88592a4d71e64990133e86f"

REQUEST_TYPE = usb.util.build_request_type(
    usb.util.CTRL_OUT, usb.util.CTRL_TYPE_VENDOR, usb.util.CTRL_RECIPIENT_DEVICE)


def extract_firmware():
    blocks = []
    with open("Lmcv2u.sys", "rb") as f:

        hash = hashlib.md5(f.read()).hexdigest()

        if hash != KNOWN_HASH:
            print(f"Error, Lmcu2v.sys md5 hash does not match the version this tool was written for")
            print(f"    Your value : {hash}")
            print(f"    Known value: {KNOWN_HASH}")
            exit(1)

        f.seek(0x4440)
        while True:
            block = f.read(22)
            length, value, end, data = struct.unpack("BxHB16sx", block)
            if end != 0:
                break
            blocks.append((value, data[:length]))
    return blocks


blocks = extract_firmware()

# Find the device
# 0x9588 0x9980
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if not dev:
    print(f"Could not find the usb devcie 0x{VENDOR_ID:04x}:0x{PRODUCT_ID:04x}")
    print(f"    Make sure your laser is plugged in and not already initialized")
    exit(1)


# Start Firmware transfer
dev.ctrl_transfer(REQUEST_TYPE, bRequest=0xa0, wValue=0xe600,
                  wIndex=0x0, data_or_wLength=b"\x01")

# Write the firmware blocks
for block in blocks:
    dev.ctrl_transfer(REQUEST_TYPE, bRequest=0xa0,
                      wValue=block[0], wIndex=0x0, data_or_wLength=block[1])

# Complete firmware transfer
dev.ctrl_transfer(REQUEST_TYPE, bRequest=0xa0, wValue=0xe600,
                  wIndex=0x0, data_or_wLength=b"\x00")

print(f"All done, your laser should now re-enumerate with idVendor=9588, idProduct=9899")