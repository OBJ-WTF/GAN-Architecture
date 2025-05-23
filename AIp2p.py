import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageGrab
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow_examples.models.pix2pix import pix2pix
from glob import glob

CANVAS_SIZE = 256
GRID_SIZE = 16
COLOR_MAP = {
    "Noir": "#000000",
    "Blanc": "#FFFFFF",
    "Rouge": "#FF0000",
    "Vert": "#00FF00"
}

class GANApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pix2Pix Floorplan Tool")
        self.root.geometry("1000x600")
        self.root.configure(bg="#1e1e1e")
        self.current_color = "#000000"
        self.model_path = tk.StringVar()
        self.model2_path = tk.StringVar()

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TButton", padding=6, relief="flat",
                        background="#2e2e2e", foreground="#ffffff")
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TNotebook", background="#1e1e1e", foreground="#ffffff")
        style.map("TButton",
                  background=[("active", "#3e3e3e")])

        self.setup_tabs()
        self.setup_console_log()

    def styled_button(self, master, **kwargs):
        return tk.Button(master, relief="flat", borderwidth=0, highlightthickness=0,
                         bg="#2e2e2e", fg="white", activebackground="#3e3e3e",
                         font=("Segoe UI", 10), padx=10, pady=5,
                         **kwargs)

    def setup_console_log(self):
        self.console_text = tk.Text(self.root, height=8, bg="#121212", fg="#CCCCCC",
                                    insertbackground="white", relief="flat")
        self.console_text.pack(fill="x", side="bottom", padx=5, pady=2)
        import sys
        class ConsoleRedirect:
            def __init__(self, console_widget):
                self.console_widget = console_widget
            def write(self, msg):
                self.console_widget.insert(tk.END, msg)
                self.console_widget.see(tk.END)
            def flush(self):
                pass
        sys.stdout = sys.stderr = ConsoleRedirect(self.console_text)

    def setup_tabs(self):
        notebook = ttk.Notebook(self.root)
        self.generate_tab = ttk.Frame(notebook)
        self.train_tab = ttk.Frame(notebook)

        notebook.add(self.generate_tab, text="Génération")
        notebook.add(self.train_tab, text="Entraînement")
        notebook.pack(fill="both", expand=True)

        self.setup_generation_ui(self.generate_tab)
        self.setup_training_ui(self.train_tab)

    def setup_generation_ui(self, frame):
        main_frame = tk.Frame(frame, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#1e1e1e")
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        right_frame = tk.Frame(main_frame, bg="#1e1e1e")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(left_frame, text="Canvas de dessin (256x256)", bg="#1e1e1e", fg="white").pack()
        self.canvas = tk.Canvas(left_frame, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white", bd=0, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_preview)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<Button-3>", self.delete_shape)

        color_frame = tk.LabelFrame(left_frame, text="Couleurs", bg="#1e1e1e", fg="white")
        color_frame.pack(pady=5)
        for name, color in COLOR_MAP.items():
            tk.Button(color_frame, bg=color, width=3, command=lambda c=color: self.set_color(c)).pack(side=tk.LEFT, padx=2)

        self.styled_button(left_frame, text="Importer Image", command=self.import_image).pack(pady=5)
        self.styled_button(left_frame, text="Effacer", command=self.clear_canvas).pack(pady=5)

        tk.Label(left_frame, text="Modèle principal (.h5)", bg="#1e1e1e", fg="white").pack(pady=2)
        self.styled_button(left_frame, text="Sélectionner modèle 1", command=self.choose_model).pack()

        tk.Label(left_frame, text="Modèle secondaire (.h5)", bg="#1e1e1e", fg="white").pack(pady=2)
        self.styled_button(left_frame, text="Sélectionner modèle 2", command=self.choose_second_model).pack()

        self.styled_button(left_frame, text="Générer", command=self.transfer_generate).pack(pady=10)
        self.gen_bar = ttk.Progressbar(left_frame, length=200, mode='determinate')
        self.gen_bar.pack(pady=5)

        image_frame = tk.Frame(right_frame, bg="#1e1e1e")
        image_frame.pack(fill="both", expand=True)

        self.output_label = tk.Label(image_frame, text="Résultat final", bg="#1e1e1e", fg="white")
        self.output_label.pack(pady=10)

        self.intermediate_label = tk.Label(image_frame, text="Image intermédiaire", bg="#1e1e1e", fg="white")
        self.intermediate_label.pack(pady=10)

    def setup_training_ui(self, frame):
        tk.Label(frame, text="Dossier des images d'entrée (A)", bg="#1e1e1e", fg="white").pack()
        self.input_path = tk.Entry(frame, width=50)
        self.input_path.pack()
        self.styled_button(frame, text="Parcourir", command=lambda: self.input_path.insert(0, filedialog.askdirectory())).pack()

        tk.Label(frame, text="Dossier des images cibles (B)", bg="#1e1e1e", fg="white").pack()
        self.target_path = tk.Entry(frame, width=50)
        self.target_path.pack()
        self.styled_button(frame, text="Parcourir", command=lambda: self.target_path.insert(0, filedialog.askdirectory())).pack()

        tk.Label(frame, text="Nombre d'époques (ex: 50)", bg="#1e1e1e", fg="white").pack()
        self.epoch_entry = tk.Entry(frame, width=10)
        self.epoch_entry.pack()

        self.progress_bar = ttk.Progressbar(frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5)
        self.styled_button(frame, text="Lancer l'entraînement", command=self.start_training).pack(pady=10)

    def set_color(self, color):
        self.current_color = color

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.current_color)
        self.canvas.itemconfig(self.current_rect, tags="shape")

    def draw_preview(self, event):
        if hasattr(self, 'current_rect'):
            self.canvas.coords(self.current_rect, self.start_x, self.start_y, event.x, event.y)

    def end_draw(self, event):
        if hasattr(self, 'current_rect'):
            self.canvas.itemconfig(self.current_rect, fill=self.current_color, outline=self.current_color)
            self.current_rect = None

    def delete_shape(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if "shape" in self.canvas.gettags(item):
            self.canvas.delete(item)

    def clear_canvas(self):
        self.canvas.delete("all")

    def import_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if not path:
            return
        img = Image.open(path).resize((CANVAS_SIZE, CANVAS_SIZE))
        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

    def choose_model(self):
        path = filedialog.askopenfilename(filetypes=[("Keras Models", "*.h5")])
        if path:
            self.model_path.set(path)

    def choose_second_model(self):
        path = filedialog.askopenfilename(filetypes=[("Keras Models", "*.h5")])
        if path:
            self.model2_path.set(path)

    def save_canvas_to_image(self, filename="canvas_input.png"):
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        img = ImageGrab.grab().crop((x, y, x1, y1)).resize((CANVAS_SIZE, CANVAS_SIZE))
        img.save(filename)
        return filename

    def get_unique_output_path(self):
        from datetime import datetime
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        i = 1
        while True:
            path = f"output/generated_{timestamp}_{i:03d}.png"
            if not os.path.exists(path):
                return path
            i += 1

    def transfer_generate(self):
        model_file = self.model_path.get()
        model2_file = self.model2_path.get()

        if not model_file:
            return messagebox.showerror("Erreur", "Modèle principal non sélectionné.")

        try:
            self.gen_bar['value'] = 10
            img_path = self.save_canvas_to_image()
            self.gen_bar['value'] = 30

            output1 = self.generate_from_image(img_path, model_file)
            intermediate_path = self.get_unique_output_path().replace("generated_", "intermediate_")
            cv2.imwrite(intermediate_path, output1)

            inter_img_disp = Image.fromarray(cv2.cvtColor(output1, cv2.COLOR_BGR2RGB)).resize((CANVAS_SIZE, CANVAS_SIZE))
            inter_img_tk = ImageTk.PhotoImage(inter_img_disp)
            self.intermediate_label.config(image=inter_img_tk)
            self.intermediate_label.image = inter_img_tk

            if model2_file:
                temp_path = "output/temp_step1.png"
                cv2.imwrite(temp_path, output1)
                output2 = self.generate_from_image(temp_path, model2_file)
                final_output = output2
            else:
                final_output = output1

            self.gen_bar['value'] = 80
            output_path = self.get_unique_output_path()
            cv2.imwrite(output_path, final_output)

            img_disp = Image.fromarray(cv2.cvtColor(final_output, cv2.COLOR_BGR2RGB)).resize((CANVAS_SIZE, CANVAS_SIZE))
            img_tk = ImageTk.PhotoImage(img_disp)
            self.output_label.config(image=img_tk)
            self.output_label.image = img_tk

            self.gen_bar['value'] = 100

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def generate_from_image(self, image_path, model_path):
        model = load_model(model_path, compile=False)
        img = cv2.imread(image_path)
        img = (cv2.resize(img, (CANVAS_SIZE, CANVAS_SIZE)) / 255.0).astype(np.float32)
        tensor = np.expand_dims(img, axis=0)
        output = model.predict(tensor)[0]
        return (output * 255).astype(np.uint8)

    def start_training(self):
        input_dir = self.input_path.get()
        target_dir = self.target_path.get()
        epochs = self.epoch_entry.get()
        if not input_dir or not target_dir or not epochs:
            return messagebox.showerror("Erreur", "Champs manquants.")
        threading.Thread(target=self.run_training, args=(input_dir, target_dir, int(epochs))).start()

    def run_training(self, input_dir, target_dir, epochs):
        def load_image_pair(input_path, target_path):
            input_path = input_path.decode() if isinstance(input_path, bytes) else input_path
            target_path = target_path.decode() if isinstance(target_path, bytes) else target_path
            input_img = cv2.imread(input_path)
            target_img = cv2.imread(target_path)
            input_img = (cv2.resize(input_img, (CANVAS_SIZE, CANVAS_SIZE)) / 255.0).astype(np.float32)
            target_img = (cv2.resize(target_img, (CANVAS_SIZE, CANVAS_SIZE)) / 255.0).astype(np.float32)
            return input_img, target_img

        def load_dataset(input_dir, target_dir):
            input_paths = sorted(glob(os.path.join(input_dir, '*.png')))
            target_paths = sorted(glob(os.path.join(target_dir, '*.png')))
            dataset = tf.data.Dataset.from_tensor_slices((input_paths, target_paths))

            def process_paths(input_path, target_path):
                input_img, target_img = tf.numpy_function(
                    load_image_pair, [input_path, target_path], [tf.float32, tf.float32]
                )
                input_img.set_shape([CANVAS_SIZE, CANVAS_SIZE, 3])
                target_img.set_shape([CANVAS_SIZE, CANVAS_SIZE, 3])
                return input_img, target_img

            return dataset.map(process_paths, num_parallel_calls=tf.data.AUTOTUNE).batch(16).prefetch(tf.data.AUTOTUNE)

        def build_pix2pix():
            generator = pix2pix.unet_generator(3, norm_type='batchnorm')
            discriminator = pix2pix.discriminator(norm_type='batchnorm', target=True)
            loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)

            def generator_loss(disc_output, gen_output, target):
                gan_loss = loss_object(tf.ones_like(disc_output), disc_output)
                l1_loss = tf.reduce_mean(tf.abs(target - gen_output))
                return gan_loss + (100 * l1_loss)

            def discriminator_loss(real_output, generated_output):
                real_loss = loss_object(tf.ones_like(real_output), real_output)
                fake_loss = loss_object(tf.zeros_like(generated_output), generated_output)
                return real_loss + fake_loss

            return generator, discriminator, generator_loss, discriminator_loss

        @tf.function
        def train_step(input_image, target, generator, discriminator,
                       generator_optimizer, discriminator_optimizer,
                       generator_loss, discriminator_loss):
            with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
                gen_output = generator(input_image, training=True)
                disc_real_output = discriminator([input_image, target], training=True)
                disc_generated_output = discriminator([input_image, gen_output], training=True)

                gen_loss = generator_loss(disc_generated_output, gen_output, target)
                disc_loss = discriminator_loss(disc_real_output, disc_generated_output)

            gen_grads = gen_tape.gradient(gen_loss, generator.trainable_variables)
            disc_grads = disc_tape.gradient(disc_loss, discriminator.trainable_variables)
            generator_optimizer.apply_gradients(zip(gen_grads, generator.trainable_variables))
            discriminator_optimizer.apply_gradients(zip(disc_grads, discriminator.trainable_variables))

        dataset = load_dataset(input_dir, target_dir)
        generator, discriminator, gen_loss, disc_loss = build_pix2pix()
        gen_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
        disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

        for epoch in range(epochs):
            for input_image, target in dataset:
                train_step(input_image, target, generator, discriminator,
                           gen_opt, disc_opt, gen_loss, disc_loss)
            self.progress_bar['value'] = ((epoch + 1) / epochs) * 100
            print(f"✅ Epoch {epoch + 1} terminée")

        model_dir = os.path.join(os.getcwd(), "models")
        os.makedirs(model_dir, exist_ok=True)

        i = 1
        while True:
            model_name = f"floorplan_generator_{i:03d}.h5"
            model_path = os.path.join(model_dir, model_name)
            if not os.path.exists(model_path):
                break
            i += 1

        generator.save(model_path)
        print(f"✅ Modèle sauvegardé : {model_path}")
        messagebox.showinfo("Terminé", f"Modèle entraîné et sauvegardé dans :\n{model_path}")

if __name__ == '__main__':
    root = tk.Tk()
    app = GANApp(root)
    root.mainloop()
