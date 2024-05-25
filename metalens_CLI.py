import exifread
from PIL import Image
import os
import datetime


base_file_name = "metalens_"
i = 1  # Starting counter

try:
    image_name = input("Enter Image file name with extension: ") # Input image name 
    if image_name.lower().endswith((".jpg", ".jpeg", ".tiff", ".tif")):
        image1 = Image.open(image_name)

        width=200
        height=200
        resized_image=image1.resize((width,height)) # Resizing Image
        display_image = resized_image.show()  # Display Image

    img = open(image_name, 'rb')  # giving 'reading in binary' permission

    exifdata = exifread.process_file(img)

    if exifdata:
        output_in_txt = f"{base_file_name}{i}.txt"
        while os.path.exists(output_in_txt):
            i += 1  # Incrementing counter value
            output_in_txt = f"{base_file_name}{i}.txt"

        file_name=open(output_in_txt,"w")

        file_name.write(f"### METADATA FOR '{image_name}' ###\n------------------------------------------------------------\n")

        # Write additional file info
        file_size_mb = os.path.getsize(image_name) / (1024 * 1024)
        file_creation_date = datetime.datetime.fromtimestamp(os.path.getctime(image_name)).strftime('%d-%m-%Y %H:%M:%S')
        file_modify_date = datetime.datetime.fromtimestamp(os.path.getmtime(image_name)).strftime('%d-%m-%Y %H:%M:%S')
        file_access_date = datetime.datetime.fromtimestamp(os.path.getatime(image_name)).strftime('%d-%m-%Y %H:%M:%S')
        file_type = image_name.split('.')[-1].upper()
        file_type_extension = image_name.split('.')[-1].lower()
        mime_type = f"image/{image_name.split('.')[-1].lower()}"
        exif_byte_order = ""


        file_name.write(f"FileSize {' ' * 41}:{file_size_mb:.3f} MB\n")
        file_name.write(f"Last Download/Copy Date {' ' * 26}:{file_creation_date} GMT+6.00\n")
        file_name.write(f"FileModifyDate {' ' * 35}:{file_modify_date} GMT+6.00\n")
        file_name.write(f"FileAccessDate {' ' * 35}:{file_access_date} GMT+6.00\n")
        file_name.write(f"FileType {' ' * 41}:{file_type}\n")
        file_name.write(f"FileTypeExtension {' ' * 32}:{file_type_extension}\n")
        file_name.write(f"MIMEType {' ' * 41}:{mime_type}\n")
        file_name.write(f"ExifByteOrder {' ' * 36}:333{exif_byte_order}\n")

        print(" ")
        print(f"File Size {' '* 40}:{file_size_mb:.3f} MB \n")
        print(f"Last Download/Copy Date {' ' * 26}:{file_creation_date} GMT+6.00\n")
        print(f"FileModifyDate {' ' * 35}:{file_modify_date} GMT+6.00\n")
        print(f"Last FileAccessDate {' ' * 30}:{file_access_date} GMT+6.00\n")
        print(f"FileType {' ' * 41}:{file_type}\n")
        print(f"FileTypeExtension {' ' * 32}:{file_type_extension}\n")
        print(f"MIMEType {' ' * 41}:{mime_type}\n")
        print(f"ExifByteOrder {' ' * 36}:333{exif_byte_order}\n")

        
        # Write EXIF data
        for key, value in exifdata.items():
            if key != "JPEGThumbnail":
                file_name.write(f"{key:50}:{value}\n")  # Write to Text format
                print(f"{key:50}:{value}")

        print(f"...<File saved in {output_in_txt}>...")
    else:
        print("No EXIF data found.")

    img.close()

except FileNotFoundError:
    print(f"Oops!! Can't find '{image_name}'")
