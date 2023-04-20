import os
from PIL import Image, ImageDraw, ImageFont


def group_image(img_path):
    _pixel_spacing = 200
    _num_images = 6
    _image_width = 1000

    # get file name and open image
    img_name = img_path.split("/")[1].split(".")[0]
    img = Image.open(img_path)

    # convert image to desired image width
    w, h = img.size
    scale = _image_width / w
    img = img.resize((int(w * scale), int(h * scale)))

    # Create blank canvas based on desired width and pixel spacing
    canvas = Image.new(
        "RGBA",
        (
            _image_width * _num_images + _pixel_spacing * (_num_images + 1),    # width
            _pixel_spacing*4 + img.height*3,                                    # height
        ),
        color=(255, 255, 255),
    )

    for i in range(2, _num_images + 2):
        # COLOR IMAGE
        output_img = img.quantize(colors=i)
        canvas.paste(
            output_img,
            box=(
                (i - 2) * (_image_width + _pixel_spacing) + _pixel_spacing, # width positioning
                _pixel_spacing,                                             # height positioning
            ),
        )

        # BLACK AND WHITE IMAGE
        img_bw = img.convert("L").quantize(colors=i)
        canvas.paste(
            img_bw,
            box=(
                (i - 2) * (_image_width + _pixel_spacing) + _pixel_spacing, # width positioning
                _pixel_spacing*2 + img_bw.height,                           # height
            ),
        )
        #PIXELATED IMAGE
        img_pxl = pixelate(img, int(160/i))
        canvas.paste(
            img_pxl,
            box=(
                (i - 2) * (_image_width + _pixel_spacing) + _pixel_spacing, # width positioning
                _pixel_spacing*3 + img_bw.height*2,                           # height
            ),
        )

        # Add annotations
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype("FreeMono.ttf", 100)
        draw.text((20, 20), "Country: " + i, 
        fill = (0, 0, 0, 255), font = font)

    canvas.save("output/" + img_name + ".png")

def pixelate(image, pixel_size):
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the number of pixels in each row and column
    num_cols = int(width / pixel_size)
    num_rows = int(height / pixel_size)

    # Resize the image to the desired pixel size
    img_out = Image.new(mode="RGB", size=(image.size))

    # Iterate over each pixel block and set the color to the average color of the block
    for y in range(0, num_rows):
        for x in range(0, num_cols):
            # Get the color of the pixel block
            box = (x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size)
            pixels = image.crop(box).getdata()
            avg_color = tuple(map(lambda x: int(sum(x) / len(x)), zip(*pixels)))

            # Set the color of the pixel block to the average color
            for i in range(pixel_size):
                for j in range(pixel_size):
                    img_out.putpixel((x * pixel_size + i, y * pixel_size + j), avg_color)

    return img_out

# run function
group_image("images/willie.png")