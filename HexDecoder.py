import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import struct
import numpy as np
from PIL import Image, ImageTk
import os
import math


def clean_hex_data(data):
    return ''.join(c for c in data if c in '0123456789abcdefABCDEF')

def hex_to_float32_le(hex_str):
    cleaned = clean_hex_data(hex_str)
    floats = []
    for i in range(0, len(cleaned), 8):
        chunk = cleaned[i:i+8]
        if len(chunk) == 8:
            b = bytes.fromhex(chunk)
            floats.append(str(struct.unpack('<f', b)[0]))
    return ', '.join(floats)

def float32_to_hex_le(floats_str):
    hexes = []
    for val in floats_str.split(','):
        try:
            f = float(val.strip())
            b = struct.pack('<f', f)
            hexes.append(b.hex())
        except:
            pass
    return ' '.join(hexes)

def hex_to_int16_le(hex_str):
    cleaned = clean_hex_data(hex_str)
    ints = []
    for i in range(0, len(cleaned), 4):
        chunk = cleaned[i:i+4]
        if len(chunk) == 4:
            b = bytes.fromhex(chunk)
            ints.append(str(struct.unpack('<h', b)[0]))
    return ', '.join(ints)

def int16_to_hex_le(ints_str):
    hexes = []
    for val in ints_str.split(','):
        try:
            i = int(val.strip())
            b = struct.pack('<h', i)
            hexes.append(b.hex())
        except:
            pass
    return ' '.join(hexes)

def hex_to_little_endian(hex_str):
    cleaned = clean_hex_data(hex_str)
    result = []
    for i in range(0, len(cleaned), 2):
        result.append(cleaned[i:i+2])
    return ' '.join(reversed(result))

def little_endian_to_hex(le_str):
    parts = le_str.split()
    return ''.join(reversed(parts))

def visualize_data(data_str, mode):
    try:
        values = [float(v.strip()) for v in data_str.split(',') if v.strip() != '']
        if not values:
            raise ValueError("No valid numbers to visualize.")

        vmin = min(values)
        vmax = max(values)
        if vmax == vmin:
            vmax += 1  # prevent division by zero

        length = len(values)
        size = int(np.ceil(np.sqrt(length)))
        image = np.zeros((size, size, 3), dtype=np.uint8)

        for idx, val in enumerate(values):
            y = idx // size
            x = idx % size
            if mode == 'float32':
                norm = int(((val - vmin) / (vmax - vmin)) * 255)
                image[y, x] = [norm]*3
            elif mode == 'int16':
                norm = int(((val - vmin) / (vmax - vmin)) * 255)
                if val <= vmax:
                    image[y, x] = [norm]*3
                else:
                    image[y, x] = [0, 255, 255]

        img = Image.fromarray(image).resize((size*10, size*10), Image.NEAREST)
        return ImageTk.PhotoImage(img)

    except Exception as e:
        messagebox.showerror("Visualization Error", str(e))
        return None

def set_image_from_data(data_str, mode):
    img = visualize_data(data_str, mode)
    if img:
        image_label.image = img  # сохранить ссылку, чтобы не удалился
        image_label.config(image=img)

def copy_to_clipboard(textbox):
    root.clipboard_clear()
    root.clipboard_append(textbox.get("1.0", tk.END).strip())
    root.update()

def float32_magic():
    filepath = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*")])
    if not filepath:
        return

    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        output_lines = []
        byte_line = []
        float_line = []
        i = 0

        def is_valid_float32(val, raw):
            return (
                not math.isnan(val) and not math.isinf(val)
                and abs(val) > 1e-9 and abs(val) < 64.0
                and raw != 0
            )

        while i <= len(data) - 4:
            chunk = data[i:i+4]
            raw = int.from_bytes(chunk, byteorder='little', signed=False)
            try:
                val = struct.unpack('<f', chunk)[0]
                if is_valid_float32(val, raw):
                    if byte_line:
                        output_lines.append(' '.join(byte_line))
                        byte_line = []
                    float_line.append(f"{val:.8f}")
                    i += 4
                    continue
            except:
                pass

            if float_line:
                output_lines.append(', '.join(float_line))
                float_line = []

            byte_line.append(f"{data[i]:02x}")
            i += 1

        if float_line:
            output_lines.append(', '.join(float_line))
        while i < len(data):
            byte_line.append(f"{data[i]:02x}")
            i += 1
        if byte_line:
            output_lines.append(' '.join(byte_line))

        output_path = os.path.splitext(filepath)[0] + "_decoded.txt"
        with open(output_path, 'w') as out:
            out.write('\n'.join(output_lines))

        messagebox.showinfo("Float32 Magic", f"Decoded file saved as:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Float32 Magic Error", str(e))




root = tk.Tk()
root.title("Hex Data Converter & Visualizer")
root.geometry("1000x600")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_rowconfigure(0, weight=1)

left_text = ScrolledText(frame, wrap=tk.WORD)
left_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

right_text = ScrolledText(frame, wrap=tk.WORD)
right_text.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

button_frame = tk.Frame(frame)
button_frame.grid(row=0, column=1, padx=5)

# Conversion buttons
tk.Button(button_frame, text="Hex to Float32 =>", command=lambda: right_text.delete("1.0", tk.END) or right_text.insert(tk.END, hex_to_float32_le(left_text.get("1.0", tk.END)))).pack(pady=2)
tk.Button(button_frame, text="<= Float32 to Hex", command=lambda: left_text.delete("1.0", tk.END) or left_text.insert(tk.END, float32_to_hex_le(right_text.get("1.0", tk.END)))).pack(pady=2)

tk.Button(button_frame, text="Hex to SignedInt16 =>", command=lambda: right_text.delete("1.0", tk.END) or right_text.insert(tk.END, hex_to_int16_le(left_text.get("1.0", tk.END)))).pack(pady=2)
tk.Button(button_frame, text="<= SignedInt16 to Hex", command=lambda: left_text.delete("1.0", tk.END) or left_text.insert(tk.END, int16_to_hex_le(right_text.get("1.0", tk.END)))).pack(pady=2)

tk.Button(button_frame, text="Hex to Little Endian =>", command=lambda: right_text.delete("1.0", tk.END) or right_text.insert(tk.END, hex_to_little_endian(left_text.get("1.0", tk.END)))).pack(pady=2)
tk.Button(button_frame, text="<= Little Endian to Hex", command=lambda: left_text.delete("1.0", tk.END) or left_text.insert(tk.END, little_endian_to_hex(right_text.get("1.0", tk.END)))).pack(pady=2)

# Copy buttons
tk.Button(frame, text="Copy", command=lambda: copy_to_clipboard(left_text)).grid(row=1, column=0, pady=5)
tk.Button(frame, text="Copy", command=lambda: copy_to_clipboard(right_text)).grid(row=1, column=2, pady=5)

# Image display and visualizer controls
image_label = tk.Label(root)
image_label.grid(row=1, column=0, pady=10)

visualize_frame = tk.Frame(root)
visualize_frame.grid(row=2, column=0, pady=5)

# Visualize buttons
tk.Button(visualize_frame, text="Float32 Magic", command=float32_magic).pack(side=tk.LEFT, padx=5)
tk.Button(visualize_frame, text="Visualize Float32", command=lambda: set_image_from_data(right_text.get("1.0", tk.END), 'float32')).pack(side=tk.LEFT, padx=5)
tk.Button(visualize_frame, text="Visualize Int16", command=lambda: set_image_from_data(right_text.get("1.0", tk.END), 'int16')).pack(side=tk.LEFT, padx=5)

root.mainloop()
