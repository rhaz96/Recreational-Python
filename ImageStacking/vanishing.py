import os
from PIL import Image
import numpy as np

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

merged_data = list(zip(*list(medians.values())))
stacked = Image.new("RGB", (464, 348))
stacked.putdata(merged_data)
stacked.show()
stacked.save("train_gone.tif", "TIFF")

