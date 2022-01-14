from pypylon import pylon # pip install pypylon

Converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
Converter.OutputPixelFormat = pylon.PixelType_BGR8packed
Converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

def convert(grabResult):
    image = Converter.Convert(grabResult)
    return image