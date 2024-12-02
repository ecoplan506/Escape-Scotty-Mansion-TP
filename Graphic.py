from PIL import Image

class Graphic:
    def __init__(self, file):
        self.image = Image.open(file)
        self.size = Image.size
    
class Sprite(Graphic):
    def crop(self, splits):
        self.sprites = [ ]
        for i in range(splits):
            sprite = self.image.crop((0,))
            self.sprites.append(sprite)
        for _ in range(splits):
            pass