import tkinter as tk



def load_image(img_path, target_size=(150, 150)):
    print()


def predict(img_path):
    print()


def load_breeds(file_path):
    print()


def open_file():
    print()


def load_display_image(img_path):
    print()



def start():
    root = tk.Tk()
    root.title("Cats")
    root.geometry("500x600")

    btn_open = tk.Button(root, text="Open Image", command=open_file)
    btn_open.pack(pady=20)

    label = tk.Label(root, text="Select an image")
    label.pack(pady=20)

    image_label = tk.Label(root)
    image_label.pack(pady=20)

    root.mainloop()