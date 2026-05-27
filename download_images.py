import os
import re
from icrawler.builtin import BingImageCrawler

import imagehash
from PIL import Image

# searches for images of a specific hair type
classes = {
    'braids': [ ],

    'coily': [ ],

    'curly': [ ],

    'locs': [ ],

    'straight': [

        'black woman long straight hair with beanie',
        'black woman silk press with beanie',
        'straight hair with brown beanie',
        'straight hair under knit beanie',
        'straight hair sticking out of beanie',
        'straight hair tucked into beanie',
        'straight hair with baseball cap',
        'straight hair with fitted hat',
        'straight hair with backwards cap',
        'black man straight hair with beanie',
        'black man straight hair with fitted cap',

        'straight ponytail with beanie',
        'straight hair bun with beanie',
        'straight hair with scarf',
        'straight hair with durag',
        'hoodie and straight hair with beanie',

        'long straight hair side profile',
        'straight hair mirror selfie',
        'straight hair close up selfie',
        'straight hair front profile',
        'straight hair outdoor natural lighting',
        'straight hair indoor lighting',
        'straight hair low light selfie',

        'black woman silk press side profile',
        'straight hair with glasses',
        'straight hair with headphones',
        'winter outfit straight hair beanie'
    ],

    'wavy': [ ]
}

#remove duplicate images
def remove_duplicates(folder_path):

    hashes = {}

    image_formats = (
        '.jpg',
        '.jpeg',
        '.png',
        '.webp'
    )

    for file_name in os.listdir(folder_path):

        if not file_name.lower().endswith(image_formats):
            continue

        path = os.path.join(folder_path, file_name)

        try:

            #open image
            image = Image.open(path)

            #create perceptual hash
            img_hash = imagehash.average_hash(image)

            #delete duplicate
            if img_hash in hashes:

                print(f'Removing duplicate: {file_name}')

                os.remove(path)

            else:
                hashes[img_hash] = file_name

        except Exception as error:

            print(f'Error checking {file_name}: {error}')

#loop through all the classes and download images
for folder, searches in classes.items():

    print(f'\nDownloading images for: {folder}...\n')

    folder_path = f'data/raw/{folder}'
    os.makedirs(folder_path, exist_ok=True)

    # download images for every keyword
    for search in searches:

        print(f'Searching the web for: {search}...')

        crawler = BingImageCrawler(
            storage={'root_dir': folder_path}
        )

        crawler.crawl(
            keyword=search,
            max_num=11,

            filters=dict(
                size='large',
                type='photo',
                license='commercial'
            )
        )

    files = os.listdir(folder_path)

    image_formats = ('.jpg', '.jpeg', '.png', '.webp')

    image_files = [
        file for file in files
        if file.lower().endswith(image_formats)
    ]

    #find highest existing numbered file
    existing_numbers = []

    for file_name in image_files:

        match = re.match(
            rf'{folder}(\d+)\.(jpg|jpeg|png|webp)$',
            file_name.lower()
        )

        if match:
            existing_numbers.append(int(match.group(1)))

    next_num = max(existing_numbers, default=0) + 1

    #rename only newly downloaded files
    for file_name in image_files:

        #skip files already named like braids23.jpg
        if re.match(
            rf'{folder}\d+\.(jpg|jpeg|png|webp)$',
            file_name.lower()
        ):
            continue

        old_path = os.path.join(folder_path, file_name)

        extension = os.path.splitext(file_name)[1].lower()

        new_path = os.path.join(
            folder_path,
            f'{folder}{next_num}{extension}'
        )

        #avoid collisions
        while os.path.exists(new_path):
            next_num += 1
            new_path = os.path.join(
                folder_path,
                f'{folder}{next_num}{extension}'
            )

        os.rename(old_path, new_path)
        next_num += 1

    #remove duplicate images
    remove_duplicates(folder_path)
    print(f'Finished downloading and renaming images for: {folder}.\n')

print('All image downloads and renaming complete.')