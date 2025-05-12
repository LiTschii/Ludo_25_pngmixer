#!/usr/bin/env python3
"""
PNG Mixer - Creates a DIN A4 format PNG from A-type and B-type images
with configurable rarity distribution.

Image Requirements:
- A-types: a.png (common), b.png (uncommon), c.png (legendary)
- B-types: xp.png (normal), xpxd.png (special)
- All images should be 500x500 PNG format
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import random
import os
import sys

class PNGMixer:
    def __init__(self, root):
        self.root = root
        self.root.title("Ludo PNG Mixer")
        self.root.geometry("800x600")
        
        # DIN A4 dimensions at 300 DPI: 2480 x 3508 pixels
        self.output_width = 2480
        self.output_height = 3508
        self.images_per_row = 6
        
        # Image paths
        self.a_type_images = {
            'common': None,      # a.png
            'uncommon': None,    # b.png
            'legendary': None    # c.png
        }
        self.b_type_images = {
            'normal': None,      # xp.png
            'special': None      # xpxd.png
        }
        
        # Loaded image objects
        self.loaded_a_images = {}
        self.loaded_b_images = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image loading section
        ttk.Label(main_frame, text="Load Images", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        
        # A-type images
        ttk.Label(main_frame, text="A-Type Images:").grid(row=1, column=0, sticky=tk.W)
        
        ttk.Button(main_frame, text="Load Common (a.png)", 
                  command=lambda: self.load_image('a', 'common')).grid(row=2, column=0, pady=5, sticky=tk.W)
        ttk.Button(main_frame, text="Load Uncommon (b.png)", 
                  command=lambda: self.load_image('a', 'uncommon')).grid(row=3, column=0, pady=5, sticky=tk.W)
        ttk.Button(main_frame, text="Load Legendary (c.png)", 
                  command=lambda: self.load_image('a', 'legendary')).grid(row=4, column=0, pady=5, sticky=tk.W)
        
        # B-type images
        ttk.Label(main_frame, text="B-Type Images:").grid(row=1, column=1, sticky=tk.W, padx=(20, 0))
        
        ttk.Button(main_frame, text="Load Normal (xp.png)", 
                  command=lambda: self.load_image('b', 'normal')).grid(row=2, column=1, pady=5, sticky=tk.W, padx=(20, 0))
        ttk.Button(main_frame, text="Load Special (xpxd.png)", 
                  command=lambda: self.load_image('b', 'special')).grid(row=3, column=1, pady=5, sticky=tk.W, padx=(20, 0))
        
        # Status labels
        self.status_labels = {}
        for i, (img_type, rarity) in enumerate([('a', 'common'), ('a', 'uncommon'), ('a', 'legendary')]):
            self.status_labels[f"{img_type}_{rarity}"] = ttk.Label(main_frame, text="Not loaded", foreground="red")
            self.status_labels[f"{img_type}_{rarity}"].grid(row=2+i, column=2, padx=10)
        
        for i, (img_type, rarity) in enumerate([('b', 'normal'), ('b', 'special')]):
            self.status_labels[f"{img_type}_{rarity}"] = ttk.Label(main_frame, text="Not loaded", foreground="red")
            self.status_labels[f"{img_type}_{rarity}"].grid(row=2+i, column=3, padx=10)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=20)
        
        # Configuration section
        ttk.Label(main_frame, text="Configuration", font=("Arial", 14, "bold")).grid(row=6, column=0, columnspan=4, pady=10)
        
        # A-type distribution sliders
        ttk.Label(main_frame, text="A-Type Distribution:").grid(row=7, column=0, columnspan=4, sticky=tk.W)
        
        ttk.Label(main_frame, text="Common %:").grid(row=8, column=0, sticky=tk.W)
        self.a_common_var = tk.DoubleVar(value=70)
        self.a_common_scale = ttk.Scale(main_frame, from_=0, to=100, variable=self.a_common_var, orient="horizontal")
        self.a_common_scale.grid(row=8, column=1, sticky=(tk.W, tk.E))
        self.a_common_label = ttk.Label(main_frame, text="70%")
        self.a_common_label.grid(row=8, column=2, padx=10)
        
        ttk.Label(main_frame, text="Uncommon %:").grid(row=9, column=0, sticky=tk.W)
        self.a_uncommon_var = tk.DoubleVar(value=25)
        self.a_uncommon_scale = ttk.Scale(main_frame, from_=0, to=100, variable=self.a_uncommon_var, orient="horizontal")
        self.a_uncommon_scale.grid(row=9, column=1, sticky=(tk.W, tk.E))
        self.a_uncommon_label = ttk.Label(main_frame, text="25%")
        self.a_uncommon_label.grid(row=9, column=2, padx=10)
        
        ttk.Label(main_frame, text="Legendary %:").grid(row=10, column=0, sticky=tk.W)
        self.a_legendary_var = tk.DoubleVar(value=5)
        self.a_legendary_scale = ttk.Scale(main_frame, from_=0, to=100, variable=self.a_legendary_var, orient="horizontal")
        self.a_legendary_scale.grid(row=10, column=1, sticky=(tk.W, tk.E))
        self.a_legendary_label = ttk.Label(main_frame, text="5%")
        self.a_legendary_label.grid(row=10, column=2, padx=10)
        
        # B-type distribution slider
        ttk.Label(main_frame, text="B-Type Special Chance %:").grid(row=11, column=0, sticky=tk.W)
        self.b_special_var = tk.DoubleVar(value=10)
        self.b_special_scale = ttk.Scale(main_frame, from_=0, to=100, variable=self.b_special_var, orient="horizontal")
        self.b_special_scale.grid(row=11, column=1, sticky=(tk.W, tk.E))
        self.b_special_label = ttk.Label(main_frame, text="10%")
        self.b_special_label.grid(row=11, column=2, padx=10)
        
        # Bind scale changes to update labels
        self.a_common_scale.bind("<Motion>", lambda e: self.update_slider_labels())
        self.a_uncommon_scale.bind("<Motion>", lambda e: self.update_slider_labels())
        self.a_legendary_scale.bind("<Motion>", lambda e: self.update_slider_labels())
        self.b_special_scale.bind("<Motion>", lambda e: self.update_slider_labels())
        
        # Generate button
        ttk.Button(main_frame, text="Generate Mixed PNG", 
                  command=self.generate_mixed_image).grid(row=12, column=0, columnspan=4, pady=20)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
    def update_slider_labels(self):
        """Update the percentage labels next to sliders"""
        self.a_common_label.config(text=f"{int(self.a_common_var.get())}%")
        self.a_uncommon_label.config(text=f"{int(self.a_uncommon_var.get())}%")
        self.a_legendary_label.config(text=f"{int(self.a_legendary_var.get())}%")
        self.b_special_label.config(text=f"{int(self.b_special_var.get())}%")
        
    def load_image(self, img_type, rarity):
        """Load an image file"""
        file_path = filedialog.askopenfilename(
            title=f"Select {img_type.upper()}-type {rarity} image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Load and store the image
                if img_type == 'a':
                    self.a_type_images[rarity] = file_path
                    # Load the actual image
                    img = Image.open(file_path)
                    if img.size != (500, 500):
                        img = img.resize((500, 500), Image.Resampling.LANCZOS)
                    self.loaded_a_images[rarity] = img
                else:
                    self.b_type_images[rarity] = file_path
                    # Load the actual image
                    img = Image.open(file_path)
                    if img.size != (500, 500):
                        img = img.resize((500, 500), Image.Resampling.LANCZOS)
                    self.loaded_b_images[rarity] = img
                
                # Update status
                self.status_labels[f"{img_type}_{rarity}"].config(text="✓ Loaded", foreground="green")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
                
    def check_all_images_loaded(self):
        """Check if all required images are loaded"""
        a_loaded = all(self.loaded_a_images.get(key) is not None for key in ['common', 'uncommon', 'legendary'])
        b_loaded = all(self.loaded_b_images.get(key) is not None for key in ['normal', 'special'])
        return a_loaded and b_loaded
        
    def generate_mixed_image(self):
        """Generate the mixed PNG image"""
        if not self.check_all_images_loaded():
            messagebox.showerror("Error", "Please load all required images first!")
            return
            
        # Normalize A-type probabilities
        total_a = self.a_common_var.get() + self.a_uncommon_var.get() + self.a_legendary_var.get()
        if total_a == 0:
            messagebox.showerror("Error", "A-type probabilities cannot all be zero!")
            return
            
        a_probs = {
            'common': self.a_common_var.get() / total_a,
            'uncommon': self.a_uncommon_var.get() / total_a,
            'legendary': self.a_legendary_var.get() / total_a
        }
        
        # B-type probability
        b_special_prob = self.b_special_var.get() / 100
        
        # Calculate how many images fit
        img_width = 500  # Assuming 500x500 images
        img_height = 500
        
        # Scale images to fit DIN A4 with 6 per row
        scale_factor = self.output_width / (self.images_per_row * img_width)
        scaled_width = int(img_width * scale_factor)
        scaled_height = int(img_height * scale_factor)
        
        rows_possible = self.output_height // scaled_height
        total_images = self.images_per_row * rows_possible
        
        # Ensure A:B ratio is 1:1
        a_count = total_images // 2
        b_count = total_images - a_count
        
        # Generate A-type image list
        a_images = []
        for _ in range(a_count):
            rand = random.random()
            if rand < a_probs['common']:
                a_images.append(self.loaded_a_images['common'])
            elif rand < a_probs['common'] + a_probs['uncommon']:
                a_images.append(self.loaded_a_images['uncommon'])
            else:
                a_images.append(self.loaded_a_images['legendary'])
        
        # Generate B-type image list
        b_images = []
        for _ in range(b_count):
            if random.random() < b_special_prob:
                b_images.append(self.loaded_b_images['special'])
            else:
                b_images.append(self.loaded_b_images['normal'])
        
        # Combine and shuffle
        all_images = a_images + b_images
        random.shuffle(all_images)
        
        # Create the output image
        output_img = Image.new('RGB', (self.output_width, self.output_height), 'white')
        
        # Place images
        for i, img in enumerate(all_images):
            if i >= total_images:
                break
                
            row = i // self.images_per_row
            col = i % self.images_per_row
            
            x = col * scaled_width
            y = row * scaled_height
            
            # Scale the image
            scaled_img = img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
            output_img.paste(scaled_img, (x, y))
        
        # Save the image
        save_path = filedialog.asksaveasfilename(
            title="Save mixed PNG",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if save_path:
            output_img.save(save_path)
            messagebox.showinfo("Success", f"Image saved successfully!\n\nStats:\n- Total images: {total_images}\n- A-type: {a_count}\n- B-type: {b_count}")

def main():
    root = tk.Tk()
    app = PNGMixer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
