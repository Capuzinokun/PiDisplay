import tkinter as tk
import datahandler
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime, timedelta

class ImageWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Image Window")
        # Set the size and position of the side window
        self.attributes('-fullscreen', False)
        self.geometry('800x600')
        self.configure(bg="black")
        
        # Create a label for displaying the image
        self.image_label = tk.Label(self)
        self.image_label.pack()
        
        self.thread = threading.Thread(target=self.image_thread_functions)
        self.last_update = datetime.now()
        self.stop_signal = False
        self.index = 0
        
        self.dh = datahandler.DataHandler()
        
        def destroy_window(event):
            self.stop_signal = True
            self.thread.join()
            self.destroy()
        self.bind('<Escape>', destroy_window)
        
        def toggle_fullscreen(event=None):
            if self.attributes('-fullscreen'):
                self.attributes('-fullscreen', False)
                self.geometry('800x600')  # Set your desired smaller size
            else:
                self.attributes('-fullscreen', True)
        self.bind('<f>', toggle_fullscreen)
        
        def fetch_and_update_images(event):
            self.stop_signal = True
            if self.thread.is_alive():
                print("Waiting for thread to end")
                self.thread.join()
            self.stop_signal = False
            self.thread = threading.Thread(target=self.image_thread_functions)
            self.last_update = datetime.now()
            self.thread.start()
        self.bind('<r>', fetch_and_update_images)
        
    def fetch_and_update_images(self):
        self.stop_signal = True
        if self.thread.is_alive():
            print("Waiting for thread to end")
            self.thread.join()
        self.stop_signal = False
        self.thread = threading.Thread(target=self.image_thread_functions)
        self.last_update = datetime.now()
        self.thread.start()
        
    def image_thread_functions(self):
        self.dh.fetch_images()
        self.dh.load_images()
        while self.stop_signal == False:
            self.update_images()
            
            current_time = datetime.now()
            if current_time - self.last_update >= timedelta(minutes=10):
                print("10 minutes has passed!")
                self.last_update = datetime.now()
                self.dh.fetch_images()
                self.dh.load_images()
    
    def update_images(self):
        
        print(self.stop_signal)
        print(self.dh.loaded_images)
        
        img = self.dh.loaded_images[self.index]
    
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        image_ratio = img.width / img.height
        window_ratio = screen_width / screen_height

        if window_ratio > image_ratio:
            # Fit the image to the height
            new_width = int(screen_height * image_ratio)
            new_height = screen_height
        else:
            # Fit the image to the width
            new_width = screen_width
            new_height = int(screen_width / image_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)  # Adjust the size as per your preference
        
        x_offset = (screen_width - new_width) // 2
        y_offset = (screen_height - new_height) // 2
        
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk
        
        self.image_label.place(x=x_offset, y=y_offset)
        
        self.index = (self.index + 1) if self.index + 1 < len(self.dh.loaded_images) else 0
        
        time.sleep(10) # Update image every 10 seconds