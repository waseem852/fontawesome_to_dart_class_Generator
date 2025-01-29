import tkinter as tk
from tkinter import filedialog, messagebox
from fontTools.ttLib import TTFont
import os

class FontIconGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Font Awesome Icon Generator")
        self.root.geometry("500x300")

        self.font_file_path = ""
        self.font_family_name = ""
        self.output_directory = ""

        self.create_widgets()

    def create_widgets(self):
        # Font file selection
        self.lbl_font_file = tk.Label(self.root, text="Font File:")
        self.lbl_font_file.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.txt_font_file = tk.Entry(self.root, width=40)
        self.txt_font_file.grid(row=0, column=1, padx=10, pady=10)
        
        self.btn_select_font_file = tk.Button(self.root, text="Browse", command=self.select_font_file)
        self.btn_select_font_file.grid(row=0, column=2, padx=10, pady=10)

        # Font Family name
        self.lbl_font_family = tk.Label(self.root, text="Font Family Name:")
        self.lbl_font_family.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.txt_font_family = tk.Entry(self.root, width=40)
        self.txt_font_family.grid(row=1, column=1, padx=10, pady=10)
        
        # Output directory
        self.lbl_output_dir = tk.Label(self.root, text="Output Directory:")
        self.lbl_output_dir.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.txt_output_dir = tk.Entry(self.root, width=40)
        self.txt_output_dir.grid(row=2, column=1, padx=10, pady=10)
        
        self.btn_select_output_dir = tk.Button(self.root, text="Browse", command=self.select_output_dir)
        self.btn_select_output_dir.grid(row=2, column=2, padx=10, pady=10)

        # Generate class button
        self.btn_generate_class = tk.Button(self.root, text="Generate Dart Class", command=self.generate_class)
        self.btn_generate_class.grid(row=3, column=1, padx=10, pady=20)

    def select_font_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("TrueType Fonts", "*.ttf")])
        if file_path:
            self.font_file_path = file_path
            self.txt_font_file.delete(0, tk.END)
            self.txt_font_file.insert(0, file_path)

    def select_output_dir(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_directory = folder_path
            self.txt_output_dir.delete(0, tk.END)
            self.txt_output_dir.insert(0, folder_path)

    def generate_class(self):
        self.font_family_name = self.txt_font_family.get()

        if not self.font_file_path or not self.font_family_name or not self.output_directory:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            self.create_dart_class()
            messagebox.showinfo("Success", "Dart class generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_dart_class(self):
        # Read the font file
        font = TTFont(self.font_file_path)
        cmap = font["cmap"].getBestCmap()

        class_name = f"{self.font_family_name}Icons"
        class_content = f"// Generated Dart class for {self.font_family_name}\n\n"
        class_content += f"import 'package:flutter/widgets.dart';\n\n"
        class_content += f"class {class_name} {{\n"
        class_content += f"    static const String fontFamily = '{self.font_family_name}';\n\n"

        # Loop over each character in the cmap and generate Dart constants
        for unicode, name in cmap.items():
            # Ensure valid Dart variable names (start with a letter, only letters/numbers)
            dart_name = self.create_valid_dart_name(name)
            class_content += f"    static const IconData {dart_name} = IconData(0x{unicode:X}, fontFamily: fontFamily);\n"

        class_content += "}\n"

        # Save to output directory
        output_file = os.path.join(self.output_directory, f"{class_name}.dart")
        with open(output_file, "w") as f:
            f.write(class_content)

    def create_valid_dart_name(self, name):
        # Dart identifiers must start with a letter and only contain letters, numbers, and underscores
        valid_name = ''.join([c if c.isalnum() or c == '_' else '_' for c in name])
        # Ensure the name starts with a letter (if needed)
        if valid_name[0].isdigit():
            valid_name = 'icon_' + valid_name
        return valid_name

def main():
    root = tk.Tk()
    app = FontIconGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
