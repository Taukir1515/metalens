import exifread
from PIL import Image, ImageTk
import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

root = tk.Tk()
root.title("MetaLens: Image Metadata Extractor")
root.geometry("1200x800")

# Create a label for the file path entry
file_path_label = tk.Label(root, text="Select Image File:")
file_path_label.pack()

# Create an entry to display the selected file path
file_path_entry = tk.Entry(root, width=40)
file_path_entry.pack()

# Create a button to browse for a file
browse_button = tk.Button(root, text="Browse", command=lambda: file_path_entry.insert(0, filedialog.askopenfilename()))
browse_button.pack()

# Create a function to redirect printed output to the Text widget
def redirect_output(text):
    output_text_widget.insert(tk.END, text)

# Create a button to process the image and display metadata
process_button = tk.Button(root, text="Process Image", command=lambda: process_image())
process_button.pack()

# Create a Text widget to display output
output_text_widget = tk.Text(root, height=30, width=50)
output_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Scrollbar for the Text widget
text_scrollbar = tk.Scrollbar(root, command=output_text_widget.yview)
text_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
output_text_widget.config(yscrollcommand=text_scrollbar.set)

# Create a Canvas widget to display the image
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack(side=tk.RIGHT, padx=20, pady=20)

# Keep a reference to the display_image
display_image = None

# Function to process the image and display metadata
def process_image():
    global display_image
    image_name = file_path_entry.get()
    file_name = os.path.basename(image_name)

    # Clear previous metadata displayed on output_text_widget
    output_text_widget.delete(1.0, tk.END)

    # Clear previous file path entry
    file_path_entry.delete(0, tk.END)

    if file_name.lower().endswith((".jpg", ".jpeg", ".tiff", ".tif", "png")):
        try:
            image1 = Image.open(file_name)

            width = 300
            height = 300
            resized_image = image1.resize((width, height))  # Resizing Image
            display_image = ImageTk.PhotoImage(resized_image)  # Display Image

            # Clear previous image
            canvas.delete("all")

            # Display the image on the Canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=display_image)

            img = open(image_name, 'rb')  # giving 'reading in binary' permission
            exifdata = exifread.process_file(img)

            if exifdata:
                base_file_name = "metalens_"
                i = 1  # Starting counter
                output_in_txt = f"{base_file_name}{i}.txt"
                while os.path.exists(output_in_txt):
                    i = i + 1  # Incrementing counter value
                    output_in_txt = f"{base_file_name}{i}.txt"

                with open(output_in_txt, "w") as file_output:
                    file_output.write(f"### METADATA FOR '{file_name}' ###\n------------------------------------------------------------\n")

                    # Write file info
                    file_size_mb = os.path.getsize(image_name) / (1024 * 1024)
                    file_creation_date = datetime.datetime.fromtimestamp(os.path.getctime(image_name)).strftime(
                        '%d-%m-%Y %H:%M:%S')
                    file_modify_date = datetime.datetime.fromtimestamp(os.path.getmtime(image_name)).strftime(
                        '%d-%m-%Y %H:%M:%S')
                    file_access_date = datetime.datetime.fromtimestamp(os.path.getatime(image_name)).strftime(
                        '%d-%m-%Y %H:%M:%S')
                    file_type = file_name.split('.')[-1].upper()
                    file_type_extension = file_name.split('.')[-1].lower()
                    mime_type = f"image/{file_name.split('.')[-1].lower()}"
                    exif_byte_order = ""

                    file_output.write(f"FileSize {' ' * 42}:{file_size_mb:.3f} MB\n")
                    file_output.write(f"Last Download/Copy Date {' ' * 26}:{file_creation_date} GMT+6.00\n")
                    file_output.write(f"FileModifyDate {' ' * 35}:{file_modify_date} GMT+6.00\n") 
                    file_output.write(f"FileAccessDate {' ' * 35}:{file_access_date} GMT+6.00\n")
                    file_output.write(f"FileType {' ' * 41}:{file_type}\n")
                    file_output.write(f"FileTypeExtension {' ' * 32}:{file_type_extension}\n")
                    file_output.write(f"MIMEType {' ' * 41}:{mime_type}\n")
                    file_output.write(f"ExifByteOrder {' ' * 36}:333{exif_byte_order}\n")

                    # Write metadata to the output_text_widget
                    output_text_widget.insert(tk.END, f"\t Metadata for {file_name} \n")
                    output_text_widget.insert(tk.END, "\t ********************************************************************************************\n")
                    output_text_widget.insert(tk.END, f"\t File Size {' ' * 40}:{file_size_mb:.3f} MB\n")
                    output_text_widget.insert(tk.END, f"\t Last Download/Copy Date {' ' * 26}:{file_creation_date} GMT+6.00\n")
                    output_text_widget.insert(tk.END, f"\t File Modify Date {' ' * 33}:{file_modify_date} GMT+6.00\n")
                    output_text_widget.insert(tk.END, f"\t Last FileAccess Date {' ' * 29}:{file_access_date} GMT+6.00\n")
                    output_text_widget.insert(tk.END, f"\t File Type {' ' * 40}:{file_type}\n")
                    output_text_widget.insert(tk.END, f"\t File Type Extension {' ' * 30}:{file_type_extension}\n")
                    output_text_widget.insert(tk.END, f"\t MIME Type {' ' * 40}:{mime_type}\n")
                    output_text_widget.insert(tk.END, f"\t Exif Byte Order {' ' * 34}:333{exif_byte_order}\n\n")

                    # Write EXIF data
                    for key, value in exifdata.items():
                        if key != "JPEGThumbnail":
                            file_output.write(f"{key:50}:{value}\n")  # Write to Text format
                            output_text_widget.insert(tk.END, f"\t {key:50}:{value}\n")

                img.close()

                output_text_widget.insert(tk.END, f" \t ******************************************************************************************** \n")
                output_text_widget.insert(tk.END, f"...<File saved as {output_in_txt}>...\n")
                
            else:
                messagebox.showinfo("Metalens", "No EXIF data found.")

        except FileNotFoundError:
            print(f"\t Oops!! Can't find '{file_name}'")
    else:
        messagebox.showinfo("Metalens", "No EXIF data found.")


# Redirect printed output to the Text widget
sys.stdout.write = redirect_output

root.mainloop()
