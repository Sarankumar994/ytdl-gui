import json
import os
import subprocess
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename, askdirectory
class YoutubeDLGUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        self.url = ttk.StringVar(value="")
        with open("settings.json", 'r') as f:
            self.settings = json.load(f)
        self.ytdl_path = ttk.StringVar(value=self.settings["ytdl_path"])
        self.aria2c_path = ttk.StringVar(value=self.settings["aria2c_path"])
        self.output_dir = ttk.StringVar(value=self.settings["output_dir"])

        self.create_form()

    def create_form(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
    
        # URL entry
        url_lbl = ttk.Label(container, text="URL", width=10)
        url_lbl.pack(side=LEFT, padx=5)
        url_ent = ttk.Entry(container, textvariable=self.url)
        url_ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
    
        # Download button
        download_btn = ttk.Button(container, text="Download", command=self.threading_subprocess)
        download_btn.pack(side=LEFT, padx=5, fill=X)
    
        # yt-dlp path entry
        container2 = ttk.Frame(self)
        container2.pack(fill=X, expand=YES, pady=5)
        ytdlp_lbl = ttk.Label(container2, text="yt-dlp path:", width=10)
        ytdlp_lbl.pack(side=LEFT, padx=5)
        ytdlp_ent = ttk.Entry(container2, textvariable=self.ytdl_path)
        ytdlp_ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
        browse_btn = ttk.Button(container2, text="Browse", command=self.on_browse_ytdlp)
        browse_btn.pack(side=LEFT, padx=5, fill=X)
    
        # aria2c path entry
        container3 = ttk.Frame(self)
        container3.pack(fill=X, expand=YES, pady=5)
        aria2c_lbl = ttk.Label(container3, text="aria2c path:", width=10)
        aria2c_lbl.pack(side=LEFT, padx=5)
        aria2c_ent = ttk.Entry(container3, textvariable=self.aria2c_path)
        aria2c_ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
        browse_btn = ttk.Button(container3, text="Browse", command=self.on_browse_aria2c)
        browse_btn.pack(side=LEFT, padx=5, fill=X)
    
        # Output directory entry
        container4 = ttk.Frame(self)
        container4.pack(fill=X, expand=YES, pady=5)
        output_lbl = ttk.Label(container4, text="output dir:", width=10)
        output_lbl.pack(side=LEFT, padx=5)
        output_ent = ttk.Entry(container4, textvariable=self.output_dir)
        output_ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
        browse_btn = ttk.Button(container4, text="Browse", command=self.on_browse_output)
        browse_btn.pack(side=LEFT, padx=5, fill=X)
    

    def threading_subprocess(self):
        new_thread = threading.Thread(target=self.download)
        new_thread.start()
        
    def on_browse_ytdlp(self):
        path = askopenfilename(title="Select ytdlp.exe")
        with open("settings.json", "r+") as f:
            data = json.load(f)
            data["ytdl_path"] = path
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            
        self.ytdl_path.set(path)

    def on_browse_aria2c(self):
        path = askopenfilename(title="Select aria2c.exe")
        
        # Read the JSON data from the file
        with open("settings.json", "r+") as f:
            data = json.load(f)
            data["aria2c_path"] = path
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        
        self.aria2c_path.set(path)

    def on_browse_output(self):
        path = askdirectory(title="Select output dir")
        with open("settings.json", "r+") as f:
            data = json.load(f)
            data["output_dir"] = path
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.output_dir.set(path)

    def download(self):
        subprocess.run([self.ytdl_path.get(), self.url.get(), '--downloader', self.aria2c_path.get(), '-S', 'height:720', '-o', "%(title)s.%(ext)s", '-P', f"{self.output_dir.get()}/videos", '-P', f"temp:{self.output_dir.get()}/temp"])
        
if __name__ == '__main__':
    if os.path.exists("settings.json"):
        pass
    else:
        with open("settings.json", "a+") as f:
            data = {}
            data["ytdl_path"] = ""
            data["aria2c_path"] = ""
            data["output_dir"] = ""
            json.dump(data, f, indent=4)
    app = ttk.Window("YoutubeDL GUI", 'superhero',)
    YoutubeDLGUI(app)
    app.mainloop()

