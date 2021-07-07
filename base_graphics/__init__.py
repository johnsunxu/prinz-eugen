from PIL import ImageFont

class BaseGraphics:
    @staticmethod
    def getFont():
        return ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 16)
    def getFontAtSize(n):
        return ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", n)
    def getNameFont():
        return  ImageFont.truetype("resources/fonts/Trebuchet_MS.ttf", 28)
    def getBackgroundColor():
        # return "rgb(45,54,69)"
        return "rgb(51,54,53)"
    def getDarkHighlightColor():
        return "rgb(102,17,17)"
    def getHighlightColor():
        # return "rgb(166,190,191)"
        return "rgb(213,75,73)"
    def getLightHighlightColor():
        return "rgb(213,220,222)"

    def getEmbedColor():
        return 0xad4b49