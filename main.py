import os
import threading
from tkinter import Tk, filedialog, Button, Label, Entry, StringVar, OptionMenu
from tkinter import ttk
from PIL import Image

input_base = ""
selected_paths = []

# === FUNCIONES ===

def select_path():
    global input_base, selected_paths
    selected_paths.clear()

    path = filedialog.askopenfilename(title="Seleccionar imagen") or \
           filedialog.askdirectory(title="Seleccionar carpeta")

    if not path:
        status_label.config(text="⚠️ No se seleccionó ninguna ruta.")
        return

    input_base = os.path.dirname(path) if os.path.isfile(path) else path
    if os.path.isfile(path):
        selected_paths.append(path)
    else:
        for root_dir, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')):
                    selected_paths.append(os.path.join(root_dir, f))

    status_label.config(text=f"📁 Seleccionadas {len(selected_paths)} imagen(es).")

def process_single_image(path, output_base, width, out_format):
    try:
        rel_path = os.path.relpath(path, start=input_base)
        rel_folder = os.path.dirname(rel_path)
        output_folder = os.path.join(output_base, rel_folder)
        os.makedirs(output_folder, exist_ok=True)

        img = Image.open(path)
        w_percent = (width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((width, h_size), Image.LANCZOS)

        name, _ = os.path.splitext(os.path.basename(path))
        output_path = os.path.join(output_folder, f"{name}.{out_format.lower()}")

        save_kwargs = {"optimize": True, "quality": 70}
        if out_format.lower() == "png":
            save_kwargs.pop("quality", None)

        img.save(output_path, out_format.upper(), **save_kwargs)
        return f"✅ {rel_path}"
    except Exception as e:
        return f"❌ {rel_path} - {str(e)}"

def process_images():
    if not selected_paths:
        status_label.config(text="⚠️ Seleccioná primero una imagen o carpeta.")
        return

    width = int(width_var.get())
    out_format = format_var.get()
    output_base = os.path.join(input_base, "img_optimized")

    progress["maximum"] = len(selected_paths)
    progress["value"] = 0
    result_lines = []

    for i, path in enumerate(selected_paths, start=1):
        status_label.config(text=f"🛠️ Procesando imagen {i} de {len(selected_paths)}...")
        root.update_idletasks()
        result = process_single_image(path, output_base, width, out_format)
        result_lines.append(result)
        progress["value"] = i

    result_label.config(text="\n".join(result_lines[:10]) + ("\n..." if len(result_lines) > 10 else ""))
    status_label.config(text="✅ Procesamiento finalizado.")

def threaded_process():
    threading.Thread(target=process_images).start()

# === GUI ESTILO WINAMP ===

root = Tk()
root.title("Image Optimizer - z1gg1")
root.geometry("600x500")
root.configure(bg="#2b2b2b")
root.resizable(False, False)

# 🎨 Colores y estilo
bg_color = "#2b2b2b"
fg_color = "#00ff00"
entry_bg = "#3c3c3c"
entry_fg = "#00ff00"
button_bg = "#4d4d4d"
button_fg = "#00ff00"
progress_color = "#00ff00"

# 🎛️ Estilo barra de progreso
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TProgressbar", thickness=20, troughcolor="#1e1e1e", background=progress_color)

# === CONTROLES ===

Label(root, text="Ancho máximo (px):", fg=fg_color, bg=bg_color, font=("Courier", 10)).pack(pady=(10, 0))
width_var = StringVar(value="1200")
Entry(root, textvariable=width_var, width=50, bg=entry_bg, fg=entry_fg,
      insertbackground=entry_fg, relief="sunken", bd=2, font=("Courier", 10)).pack(pady=3)

Label(root, text="Formato de salida:", fg=fg_color, bg=bg_color, font=("Courier", 10)).pack(pady=(10, 0))
format_var = StringVar(value="webp")
format_menu = OptionMenu(root, format_var, "jpg", "png", "webp", "jpeg", "bmp")
format_menu.configure(bg=entry_bg, fg=entry_fg, font=("Courier", 10))
format_menu.pack(pady=3)

Button(root, text="📂 Seleccionar imagen o carpeta", command=select_path,
       width=30, bg=button_bg, fg=button_fg, activebackground="#5c5c5c",
       relief="raised", bd=2, font=("Courier", 10, "bold")).pack(pady=10)

Button(root, text="⚙️ Procesar imágenes", command=threaded_process,
       width=30, bg=button_bg, fg=button_fg, activebackground="#5c5c5c",
       relief="raised", bd=2, font=("Courier", 10, "bold")).pack(pady=5)

progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", style="TProgressbar")
progress.pack(pady=20)

status_label = Label(root, text="Esperando selección...", fg="#aaaaaa", bg=bg_color, font=("Courier", 8))
status_label.pack()

result_label = Label(root, text="", wraplength=550, justify="left", anchor="w", fg=fg_color, bg=bg_color, font=("Courier", 9))
result_label.pack(pady=10)

Label(root, text="Developed by z1gg1 - enjoy it", fg="#aaaaaa", bg=bg_color, font=("Courier", 8)).pack(pady=10)

root.mainloop()
