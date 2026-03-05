# Image Formats

# • XBGR8888 - every pixel is packed into 32-bits, with a dummy 255 value at the end, so a pixel would look like [R, G, B, 255]
# when captured in Python. (These format descriptions can seem counter-intuitive, but the underlying infrastructure tends to
# take machine endianness into account, which can mix things up!)
# • XRGB8888 - as above, with a pixel looking like [B, G, R, 255].
# • RGB888 - 24 bits per pixel, ordered [B, G, R].
# • BGR888 - as above, but ordered [R, G, B].
# • YUV420 - YUV images with a plane of Y values followed by a quarter plane of U values and then a quarter plane of V values.

