import exifread
from PIL import Image
import xml.etree.ElementTree as ET
import os


base_file_name = "metalens_"
i=1

try:
    image_name = "Enter_jpg_image.jpg"  
    image1 = Image.open(image_name)
    im=image1.show()

    img= open(image_name,'rb')

    exifdata = exifread.process_file(img)
    root = ET.Element("exif_data")
    
    if exifdata:
        for key,value in exifdata.items():
            if key!= "JPEGThumbnail":
                print(f"{key:50}:{value}") 
                   
                tag = ET.SubElement(root, key)
                tag.text = str(value)             

    else:
        print("no exifdata found") 
        
    output_file=f"{base_file_name}{i}.xml"
    while os.path.exists(output_file):
        i=i+1
        output_file=f"{base_file_name}{i}.xml"
         
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)  
    
    img.close() 
    
except FileNotFoundError:
    print(f"Oops!! Can't find '{image_name}'") 
