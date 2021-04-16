import usb.core
import usb.backend.libusb1

ABLETON_VENDOR_ID = 0x2982
PUSH2_PRODUCT_ID = 0x1967
FRAME_HEADER = [0xFF, 0xCC, 0xAA, 0x88,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00]

device = usb.core.find(idVendor=ABLETON_VENDOR_ID, idProduct=PUSH2_PRODUCT_ID)

if device is None:
    raise ValueError('ADU Device not found. Please ensure it is connected to the tablet.')

usb.util.claim_interface(device, 0)

device.set_configuration()
cfg = device.get_active_configuration()

intf = cfg[(0, 0)]
ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

ep.write(data=FRAME_HEADER)

print("done")
