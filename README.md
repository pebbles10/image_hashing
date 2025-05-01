# Image Hashing and Sorting Script

This Python script processes a folder of `.jpg` images to identify duplicates and unique images based on perceptual hashing. It organizes the images into separate folders for unique images and duplicates.

## Features

- Crops images to remove borders before processing.
- Computes perceptual hashes for images using the `imagehash` library.
- Detects duplicate images based on a configurable similarity threshold.
- Organizes images into `unique` and `duplicates` folders.
- Groups duplicates by their original image.

## Requirements

- Python 3.6 or higher
- Required Python libraries:
  - `Pillow`
  - `imagehash`

Install the dependencies using pip:

```bash
pip install Pillow imagehash 
```
Usage  
Run the script:  
```bash
python duplicates_uniques.py
```
Enter the path to the folder containing .jpg images when prompted.

The script will process the images and create a processed_images folder in the current directory with the following structure:
```
processed_images/
├── unique/
└── duplicates/
    ├── <original_image_1>/
    └──├── <dulicate_original_image>/
       ├── <dulicate_original_image>/
    ├── <original_image_2>/
    └──├── <dulicate_original_image>/
       ├── <dulicate_original_image>/
       ├── ...
```

## Configuration  
Cropping: The script crops 1200 pixels from each side of the image. You can adjust this value in the crop_box function.  
Hash Size: The hash size for perceptual hashing is set to 16 by default. You can modify it in the compute_hash function.  
Threshold: The similarity threshold for detecting duplicates is set to 5 by default. You can change it in the compare_images function.  
## Example Output  
Unique images are saved in the unique folder.  
Duplicates are grouped by their original image in the duplicates folder.  
