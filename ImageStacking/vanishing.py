import os
from PIL import Image
import numpy as np


def resize_images(dir, image, new_size):
    os.chdir(dir)
    with Image.open(image) as img:
        img_resize = img.resize(new_size, Image.ANTIALIAS)
        img_resize.save(image.split(".")[0] + "_resized.jpg", quality=95)


def get_rgb(resized_image):
    color_keys = ["red", "green", "blue"]
    color_dict = {color: [] for color in color_keys}

    for image in os.listdir():
        if "resized" in image:
            with Image.open(image) as img:
                # 0=red, 1=green, 2=blue
                for color_idx, color in enumerate(color_keys):
                    color_dict[color].append(list(img.getdata(color_idx)))
            os.remove(image)
    return color_dict


def median_pixels(image):
    medians = {color: None for color in color_keys}
    for color in medians:
        medians[color] = [
            int(np.median(col_gradient)) for col_gradient in zip(*color_dict[color])
        ]
    merged_data = list(zip(*list(medians.values())))
    return merged_data


def stack_images(image_size, stacked_img_name, img_type):
    stacked = Image.new("RGB", image_size)
    stacked.putdata(merged_data)
    stacked.show()
    stacked.save(stacked_img_name, img_type)




##########################################################################################


os.chdir("train_pics")
# store the original moon image files names here
for image in os.listdir()[1:]:
    with Image.open(image) as img:
        img_resize = img.resize((464, 348), Image.ANTIALIAS)
        img_resize.save(image.split(".")[0] + "_resized.jpg", quality=95)


# store the red, blue, and green pixels for each image here
color_keys = ["red", "green", "blue"]
color_dict = {color: [] for color in color_keys}

for image in os.listdir():
    if "resized" in image:
        with Image.open(image) as img:
            for color_idx, color in enumerate(color_keys):
                color_dict[color].append(list(img.getdata(color_idx)))
        os.remove(image)

medians = {color: None for color in color_keys}
for color in medians:
    medians[color] = [
        int(np.median(col_gradient)) for col_gradient in zip(*color_dict[color])
    ]

merged_data = list(
    zip(*list(medians.values()))
)  # list(medians.values()) has shape (5,250000)
stacked = Image.new("RGB", (464, 348))
stacked.putdata(merged_data)
stacked.show()
stacked.save("train_gone.tif", "TIFF")

# 464,348

