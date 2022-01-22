# cython: language_level=3
from pypylon import pylon # pip install pypylon

class PylonImageConvert:
    Converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    Converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    Converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def convert(grabResult):
        image = PylonImageConvert.Converter.Convert(grabResult)
        return image
