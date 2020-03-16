from PIL import Image

def jpeg_compression(image,quality):
    im = Image.open(image)
    if not im.mode == 'RGB':
        im = im.convert('RGB')
    im.save('jpeg_compressed.jpg',quality= quality)