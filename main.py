import tkinter as tk
import datahandler
import imagewindow

root = tk.Tk()
dh = datahandler.DataHandler()
root.attributes('-fullscreen', False)
root.geometry('800x600')

def refresh_image_window(event):
    global image_window
    try:
        if image_window.winfo_exists():
            pass
        else:
            image_window = imagewindow.ImageWindow(root)
    except:
        image_window = imagewindow.ImageWindow(root)
    
def destroy_root(event):
    try:
        image_window.stop_signal = True
        image_window.thread.join()
        image_window.destroy()
    except:
        pass
    finally:
        root.destroy()
        
stop_signal = False

## Keyboard Binds
root.bind('<r>', refresh_image_window)
root.bind('<Escape>', destroy_root)

root.mainloop()