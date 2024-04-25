#!/usr/bin/env python
# coding: utf-8

# In[18]:


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

class ImageToSketchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image to Sketch Converter")
        self.master.geometry("600x400")

       
        self.image = None
        self.sketch = None
        self.line_thickness = 5
        self.contrast = 1.0
        self.brightness = 1.0

       
        self.upload_btn = tk.Button(self.master, text="Upload Image", command=self.upload_image)
        self.upload_btn.grid(row=0, column=0, pady=10)

       
        self.convert_btn = tk.Button(self.master, text="Convert to Sketch", command=self.convert_to_sketch)
        self.convert_btn.grid(row=0, column=1, pady=10)

       
        self.line_thickness_label = tk.Label(self.master, text="Line Thickness")
        self.line_thickness_label.grid(row=1, column=0, pady=5)
        self.line_thickness_slider = tk.Scale(self.master, from_=1, to=20, orient=tk.HORIZONTAL, length=200, command=self.update_parameters)
        self.line_thickness_slider.set(self.line_thickness)
        self.line_thickness_slider.grid(row=1, column=1, pady=5)

        self.contrast_label = tk.Label(self.master, text="Contrast")
        self.contrast_label.grid(row=2, column=0, pady=5)
        self.contrast_slider = tk.Scale(self.master, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=200, command=self.update_parameters)
        self.contrast_slider.set(self.contrast)
        self.contrast_slider.grid(row=2, column=1, pady=5)

        self.brightness_label = tk.Label(self.master, text="Brightness")
        self.brightness_label.grid(row=3, column=0, pady=5)
        self.brightness_slider = tk.Scale(self.master, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=200, command=self.update_parameters)
        self.brightness_slider.set(self.brightness)
        self.brightness_slider.grid(row=3, column=1, pady=5)

        # Preview area
        self.preview_label = tk.Label(self.master, text="Preview")
        self.preview_label.grid(row=4, column=0, columnspan=2)
        self.preview_canvas = tk.Canvas(self.master, width=300, height=300, bg="white")
        self.preview_canvas.grid(row=5, column=0, columnspan=2)

       
        self.save_btn = tk.Button(self.master, text="Save Sketch", command=self.save_sketch)
        self.save_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg; *.jpeg; *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.show_preview(self.image)

    def convert_to_sketch(self):
        if self.image:
            
            gray_image = self.image.convert("L")
            
           
            inverted_image = ImageOps.invert(gray_image)
            blurred_image = inverted_image.filter(ImageFilter.GaussianBlur(5))
            self.sketch = ImageOps.invert(blurred_image)

            enhancer = ImageEnhance.Brightness(self.sketch)
            self.sketch = enhancer.enhance(self.brightness)
            enhancer = ImageEnhance.Contrast(self.sketch)
            self.sketch = enhancer.enhance(self.contrast)

            
            self.show_preview(self.sketch)
        else:
            tk.messagebox.showerror("Error", "Please upload an image first.")

    def save_sketch(self):
        if self.sketch:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.sketch.save(file_path)
        else:
            tk.messagebox.showerror("Error", "No sketch to save.")

    def show_preview(self, image):
        # Clear canvas
        self.preview_canvas.delete("all")

        
        img_width, img_height = image.size
        if img_width > img_height:
            new_width = 300
            new_height = int(300 * img_height / img_width)
        else:
            new_height = 300
            new_width = int(300 * img_width / img_height)
        resized_img = image.resize((new_width, new_height))

        
        self.preview_img = ImageTk.PhotoImage(resized_img)
        self.preview_canvas.create_image(150, 150, image=self.preview_img)

    def update_parameters(self, event=None):
        self.line_thickness = self.line_thickness_slider.get()
        self.contrast = self.contrast_slider.get()
        self.brightness = self.brightness_slider.get()


root = tk.Tk()
app = ImageToSketchApp(root)
root.mainloop()







