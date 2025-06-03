import os
from pathlib import Path
from PIL import Image, ImageOps
import imagehash 
import shutil
import argparse



def parse_args():
    parser = argparse.ArgumentParser(description="Image deduplication using perceptual hashing")
    parser.add_argument("--input_folder", type =str, required= True, help = "Path to the folder containing images")
    parser.add_argument("--threshold_percent", type=float, default=5.0, help="Threshold percentage for duplicate detection (default: 5.0%)")
    parser.add_argument("--padding", type=int, default=0, help="Padding for cropping (default: 0)")
    parser.add_argument("--hash_size", type=int, default=16, help="Hash size for pHash (default: 16)")
    return parser.parse_args()

args = parse_args()
HASH_SIZE = args.hash_size
THRESHOLD = args.threshold_percent
PADDING = args.padding


max_distance = HASH_SIZE * HASH_SIZE

def get_image(folder_path):
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"Invalid folder path: {folder_path}")
    images = list(folder.glob("*.jpg"))
    if not images:
        raise ValueError(f"No .jpg images found in the folder: {folder_path}")
    print(f"Found {len(images)} .jpg images in the folder.\n")
    return images

def crop_box(image, padding):
    img = Image.open(image)
    width, height = img.size

    #padding_x = width * 0.15
    #padding_y = height * 0.15
    #cropped_img = img.crop((padding_x, padding_y, width - padding_x, height - padding_y))
    #return cropped_img

    left = padding
    top = padding
    right = width - padding
    bottom = height - padding
    cropping = img.crop((left, top, right, bottom))
    cropped_img = ImageOps.exif_transpose(cropping)
    return cropped_img

def compute_hash(image, hash_size):
    image_hash = imagehash.phash(image, hash_size=hash_size)
    return image_hash

def move_to_folder(image_path, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)

    filename = os.path.basename(image_path)
    destination = os.path.join(destination_folder, filename)
    shutil.copy(image_path, destination)
    print(f"Moved: {filename} → {destination_folder}")


def find_duplicates(current_hash, unique_images, threshold):
    for previous_hash, previous_image in unique_images:
        if current_hash - previous_hash < threshold: 
            return previous_image
    return None

def compare_images(image_files, destination_folder, THRESHOLD):
    print("Comparing images...\n")

    unique_images = []
    duplicates = {}

    for current_image in image_files:
        print(f"Processing: {os.path.basename(current_image)}")
        cropping = crop_box(current_image, PADDING)
        current_hash = compute_hash(cropping, HASH_SIZE)

        matched_original = find_duplicates(current_hash, unique_images, THRESHOLD)

        if matched_original:
            print(f"Detected duplicate of: {os.path.basename(matched_original)}")
            if matched_original not in duplicates:
                duplicates[matched_original] = []
            duplicates[matched_original].append(current_image)
        else:
            print("Unique image.")
            unique_images.append((current_hash, current_image))
    
    save_images(unique_images, duplicates, destination_folder)  
    print("\nSaving files...")
    
def save_images(unique_images, duplicates, destination_folder):
    os.makedirs(os.path.join(destination_folder, "unique"), exist_ok=True)
    unique_folder = os.path.join(destination_folder, "unique")
    for _, image_file in unique_images:
        move_to_folder(image_file, unique_folder)

    duplicates_folder = os.path.join(destination_folder, "duplicates")
    os.makedirs(duplicates_folder, exist_ok=True)

    for original_image, duplicate_list in duplicates.items():
        group_folder = os.path.join(duplicates_folder, Path(original_image).stem)
        os.makedirs(group_folder, exist_ok=True)
        for image in [original_image] + duplicate_list:
            move_to_folder(image, group_folder)

    

if __name__ == "__main__":
    try:
        folder = args.input_folder
        image_list = get_image(folder)
        compare_images(image_list, destination_folder="processed_images")
        print("Done! Images sorted.")
    except Exception as e:
        print(f"Error: {e}")
    
