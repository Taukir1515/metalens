import exifread
from PIL import Image
import os


base_file_name = "metalens_"
i=1  # Starting counter

try:
    image_name = input("Enter Image file name with extension: ") 
    image1 = Image.open(image_name)
    im=image1.show() # Display Image

    img= open(image_name,'rb') # giving reading in binary permission

    exifdata = exifread.process_file(img)
 
    
    if exifdata:
        output_in_txt=f"{base_file_name}{i}.txt"
        while os.path.exists(output_in_txt):
            i=i+1 # Incrementing counter value
            output_in_txt=f"{base_file_name}{i}.txt"
        
        file_name=open(output_in_txt,"w")
        for key,value in exifdata.items():
            if key!= "JPEGThumbnail":
                file_name.write(f"{key:50}:{value}\n") # Write to Text format
                print(f"{key:50}:{value}") 
                
        print(f"<File saved in {output_in_txt}>")
                             
    else:
        print("no exifdata found")
                       
    img.close() 
    
except FileNotFoundError:
    print(f"Oops!! Can't find '{image_name}'") 
