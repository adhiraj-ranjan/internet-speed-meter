import customtkinter as ctk
import psutil
from threading import Thread
from time import sleep

class global_vars:
	last_received = psutil.net_io_counters().bytes_recv
	last_sent = psutil.net_io_counters().bytes_sent

def update():
	bytes_received = psutil.net_io_counters().bytes_recv
	bytes_sent = psutil.net_io_counters().bytes_sent

	bytes_recv_r, bytes_sent_r = bytes_received - global_vars.last_received, bytes_sent - global_vars.last_sent
	global_vars.last_received, global_vars.last_sent = bytes_received, bytes_sent
	return bytes_recv_r / 1024 / 1024, bytes_sent_r / 1024/ 1024
        	
class SpeedMeter(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("450x100")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.title("Network Speed Meter")

        self.UPDATE_FRAME_PER_SEC = 2
        # left frame
        frame_left = ctk.CTkFrame(self)
        frame_left.grid(row=0, column=0, padx=5, pady=10)

        # right frame
        frame_right = ctk.CTkFrame(self)
        frame_right.grid(row=0, column=1, padx=5, pady=10)

        # render elements in left frame
        label1 = ctk.CTkLabel(master=frame_left, text="Download", width=215)
        label1.grid(row=0, column=0, padx=0, pady=5)

        self.d_speed = ctk.CTkLabel(master=frame_left, text="", text_font=("", 20))
        self.d_speed.grid(row=1, column=0, padx=0, pady=5)

        # render elements in right frame
        label2 = ctk.CTkLabel(master=frame_right, text="Upload", width=215)
        label2.grid(row=0, column=0, padx=0, pady=5)

        self.u_speed = ctk.CTkLabel(master=frame_right, text="", text_font=("", 20))
        self.u_speed.grid(row=1, column=0, padx=0, pady=5)

        # start frame update Thread
        Thread(target=self.update_frame, daemon=True).start()
    
    def update_d_speed(self, value):
         self.d_speed.configure(text=value)
    
    def update_u_speed(self, value):
         self.u_speed.configure(text=value)
    
    def update_frame(self):
        while True:
            recv, sent = update()

            if recv < 1:
                recv_unit = 'KB/s'
                recv *= 1024
            else:
                recv_unit = 'MB/s'
            if sent < 1:
                sent_unit = 'KB/s'
                sent *= 1024
            else:
                sent_unit = 'MB/s'

            self.update_d_speed(f"{recv:.2f} {recv_unit}")
            self.update_u_speed(f"{sent:.2f} {sent_unit}")
            sleep(self.UPDATE_FRAME_PER_SEC)

    def on_closing(self, event=0):
        self.destroy()


if __name__=="__main__":
     app = SpeedMeter()
     app.mainloop()
