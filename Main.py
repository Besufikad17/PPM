import subprocess
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from .util.util import *


class App:

    def __init__(self,parent):
        self.root = parent
        self.notebook = ttk.Notebook(parent)
        self.toplevel = None
        self.installed_packages = []
        self.toplevel_ = None
        self.package_list = None
        self.btn_ = None
        self.directory = StringVar()
        self.notebook.pack()
        self.package_info = []
        self.home = Frame(self.notebook)
        self.installed = Frame(self.notebook)
        self.home_header = Frame(self.home)
        self.home_content = Frame(self.home)
        self.home_header.pack()
        self.home_content.pack()
        self.btn = ttk.Button(self.root, text='Install from requirements.txt',
                              command=self.create_install_from_requirements_content)
        self.btn.pack()
        self.installed_content = Frame(self.installed)
        self.listbox = Listbox(self.installed_content, height=8, width=50, borderwidth=0, selectborderwidth=0)
        self.installed_content.pack()
        self.notebook.add(self.home, text='Home')
        self.notebook.add(self.installed, text='Installed')
        self.name = StringVar()
        self.description = StringVar()
        self.module = StringVar()
        self.progress = StringVar()
        self.password = StringVar()
        self.MAX = 25
        self.value = DoubleVar()
        self.package_list = get_installed_packages()
        self.create_header(self.home_header)
        self.create_installed_layout(self.installed_content)

    def create_installed_layout(self, parent):
        s = subprocess.Popen('python', shell=True)
        if s.returncode is None:
            ttk.Button(parent, text='Refresh').grid(row=0, column=0, pady=20)
            ttk.Button(parent, text='Uninstall', command=self.uninstall).grid(row=0, column=1, pady=20, padx=3)
            ttk.Button(parent, text='Update', command=self.update).grid(row=0, column=2, pady=20)
            for i in range(0, len(self.package_list)):
                self.listbox.insert(i, self.package_list[i])
            self.listbox.grid(row=1, column=0, columnspan=3, rowspan=6, pady=10)
        else:
            ttk.Label(parent, text='No python version available on the system.').grid(row=0, column=0, pady=20)

    def create_header(self, parent):
        ttk.Entry(parent, width=20, textvariable=self.module).grid(row=1, column=1, padx=10, pady=20)
        ttk.Button(parent, text='search', command=self.search).grid(row=1, column=2, padx=10, pady=10)

    def create_install_from_requirements_content(self):
        self.toplevel_ = Toplevel(self.root)
        self.toplevel_.resizable(False, False)
        ttk.Entry(self.toplevel_, width=50, textvariable=self.directory).grid(row=1, column=1, padx=10, pady=20)
        self.btn = ttk.Button(self.toplevel_, text='Choose', command=self.browse).grid(row=1, column=2, padx=10, pady=10)

    def create_content(self,parent):
        ttk.Label(parent, textvariable=self.name).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(parent, textvariable=self.description, wraplength=400).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(parent, text='install', command=self.install).grid(row=2, column=1, padx=10, pady=10)

    def create_popup(self, parent, is_installation):
        self.toplevel = Toplevel(parent)
        self.toplevel.resizable(False,False)
        if is_installation:
            self.toplevel.title('Installation Progress')
            label = ttk.Label(self.toplevel, textvariable=self.progress, wraplength=400)
            progressbar = ttk.Progressbar(self.toplevel, orient=HORIZONTAL, length=200)
            progressbar.grid(row=1, column=1, padx=5, pady=5)
            progressbar.config(mode='determinate', maximum=self.MAX)
            progressbar.config(variable=self.value)
        else:
            self.toplevel.title('Uninstallation Progress')
            label = ttk.Label(self.toplevel, textvariable=self.progress)
        label.grid(row=0, column=1, padx=5, pady=5)

    def search(self):
        self.btn.destroy()
        count = 0
        index = 0
        for i in range(0, len(self.package_info)):
            if self.package_info[i]['name'] == self.module.get():
                count = count + 1
                index = i
        if count > 0:
            self.name.set(self.package_info[index]['name'] + ' ' + self.package_info[index]['version'])
            self.description.set(self.package_info[index]['description'])
            self.create_content(self.home_content)
        else:
            self.package_info.append(get_package_information(self.module.get()))
            self.name.set(self.package_info[len(self.package_info) - 1]['name'] + ' ' +
                          self.package_info[len(self.package_info) - 1]['version'])
            self.description.set(self.package_info[len(self.package_info) - 1]['description'])
            self.create_content(self.home_content)

    def install(self):
        s = subprocess.Popen('pip3 install ' + self.module.get(), shell=True, stdout=subprocess.PIPE)
        p = 0
        self.create_popup(self.home_content, True)
        console_output = read_log_file(s)
        self.MAX = len(console_output)
        try:
            for j in range(0, len(console_output)):
                p = p + 1
                unit = percentage_calculator(p, len(console_output), case=2)
                time.sleep(1)
                self.value.set(unit)
                self.progress.set(console_output[j])
                self.root.update()
            messagebox.showinfo('Info', "Process completed!")
            self.toplevel.destroy()
        except Exception as e:
            messagebox.showinfo('Info', "ERROR: {}".format(e))
            sys.exit()

    def browse(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt*")
                                                                                                , ("all files", "*.*")))
        self.directory.set(filename)
        row_= 0
        if self.directory.get() is None or self.directory.get() == '':
            messagebox.showinfo('Info', "ERROR: Choose requirements.txt file!!")
        else:
            directory = self.directory.get()
            self.package_list = read_requirements(directory)
            for i in range(0, len(self.package_list)):
                if check_installed(self.package_list[i]):
                    ch = ttk.Checkbutton(self.toplevel_, text=self.package_list[i])
                    ttk.Label(self.toplevel_, text='Installed').grid(row=i + 2, column=1)
                    ch.grid(row=i+2, column=0)
                    ch.state(['disabled'])
                    self.installed_packages.append(self.package_list[i])
                else:
                    ch = ttk.Checkbutton(self.toplevel_, text=self.package_list[i])
                    ch.grid(row=i + 2, column=0)
                    ttk.Label(self.toplevel_, text='-').grid(row=i + 2, column=1)
                row_ = i
            ttk.Button(self.toplevel_, text='Install', command=self.install_from_requirements).grid(row=row_ + 3, column=1, padx=10, pady=10)

    def install_from_requirements(self):
        self.package_list = remove_packages(self.installed_packages,self.package_list)
        for i in range(0, len(self.package_list)):
            s = subprocess.Popen('pip3 install {}'.format(self.package_list[i]), shell=True, stdout=subprocess.PIPE)
            p = 0
            self.create_popup(self.root, True)
            console_output = read_log_file(s)
            self.MAX = len(console_output)
            try:
                for j in range(0, len(console_output)):
                    p = p + 1
                    unit = percentage_calculator(p, len(console_output), case=2)
                    time.sleep(1)
                    self.value.set(unit)
                    self.progress.set(console_output[j])
                    self.root.update()
                messagebox.showinfo('Info', "Process completed!")
                self.toplevel.destroy()
            except Exception as e:
                messagebox.showinfo('Info', "ERROR: {}".format(e))
                sys.exit()

    def refresh(self):
        self.package_list = get_installed_packages()
        self.create_installed_layout(self.installed_content)
        self.root.update()

    def update(self):
        index = self.listbox.curselection()
        index = index[0]
        s = subprocess.Popen('pip3 install --upgrade ' + self.package_list[index], shell=True, stdout=subprocess.PIPE)
        p = 0
        self.create_popup(self.root, True)
        console_output = read_log_file(s)
        self.MAX = len(console_output)
        try:
            for j in range(0, len(console_output)):
                p = p + 1
                unit = percentage_calculator(p, len(console_output), case=2)
                time.sleep(1)
                self.value.set(unit)
                self.progress.set(console_output[j])
                self.root.update()
            messagebox.showinfo('Info', "Process completed!")
            self.toplevel.destroy()
        except Exception as e:
            messagebox.showinfo('Info', "ERROR: {}".format(e))
            sys.exit()

    def uninstall(self):
            index = self.listbox.curselection()
            index = index[0]
            cmd = self.package_list[index][:self.package_list[index].index(' ')]
            choose = messagebox.askyesno(message='Are you sure you want to uninstall ' + self.package_list[index] + '?')
            if choose:
                b = bytes('y', 'utf-8')
                s = subprocess.Popen('pip3 uninstall ' + cmd, shell=True, stderr=subprocess.STDOUT,
                                     stdin=subprocess.PIPE)
                p = 0
                self.create_popup(self.root, True)
                console_output = read_log_file(s, True)
                self.MAX = len(console_output)
                try:
                    for j in range(0, len(console_output)):
                        p = p + 1
                        unit = percentage_calculator(p, len(console_output), case=2)
                        time.sleep(1)
                        self.value.set(unit)
                        self.progress.set(console_output[j])
                        self.root.update()
                    messagebox.showinfo('Info', "Process completed!")
                    self.toplevel.destroy()
                    self.listbox.delete(index)
                except Exception as e:
                    messagebox.showinfo('Info', "ERROR: {}".format(e))
                    sys.exit()


def main():
    root = Tk()
    root.resizable(False, False)
    root.title('PPM')
    app = App(root)
    root.mainloop()


if __name__ == "__main__": main()
