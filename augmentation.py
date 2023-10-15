import os
from PIL import Image, ImageOps

def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

IMG_WIDTH: int = 1280
IMG_HEIGHT: int = 720

def img_remove_background(img: Image) -> Image:
    return img.crop((0, 175, IMG_WIDTH, 720))

def img_focus_robot(img: Image) -> Image:
    return crop_center(img, 400, IMG_HEIGHT)

def image_augmentation(before_path: str, after_path: str):
    os.makedirs(f"{after_path}", exist_ok=True)

    for item in os.scandir(before_path):
        if item.is_file():
            file_name = item.name
            img_default = Image.open(f"{before_path}/{file_name}")
            img_2 = ImageOps.mirror(img_default)
            img_3 = img_default.convert("L")
            img_4 = img_2.convert("L")

            rotations = [15, -15]
            for i, rotation in enumerate(rotations):
                img_default.rotate(rotation).save(f"{after_path}/{file_name[:-4]}_{i*5+3}{file_name[-4:]}")
                img_2.rotate(rotation).save(f"{after_path}/{file_name[:-4]}_{i*5+1+3}{file_name[-4:]}")
                img_3.rotate(rotation).save(f"{after_path}/{file_name[:-4]}_{i*5+2+3}{file_name[-4:]}")
                img_4.rotate(rotation).save(f"{after_path}/{file_name[:-4]}_{i*5+3+3}{file_name[-4:]}")

            img_default.save(f"{after_path}/{file_name}")
            img_2.save(f"{after_path}/{file_name[:-4]}_0{file_name[-4:]}")
            img_3.save(f"{after_path}/{file_name[:-4]}_1{file_name[-4:]}")
            img_4.save(f"{after_path}/{file_name[:-4]}_2{file_name[-4:]}")

if __name__== '__main__':
    image_augmentation("train_dataset/train_images", "train_dataset/new_images")