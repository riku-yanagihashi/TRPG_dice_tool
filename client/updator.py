import os
import socket, tkinter, platform, json, requests
import tkinter.messagebox

import application_data


class updator:
    def __init__(self, soc:socket.socket):
        self.soc = soc
        if tkinter.messagebox.askyesno(title="アップデート", message="最新のアップデートがあります。\nダウンロードしますか?"):
            self.version = application_data.version
            self.os_name = platform.system()
            self.download()
            tkinter.messagebox.showinfo(title="アップデート", message="アップデートが完了しました。\n")

    def download(self):
        self.soc.send(f"/@update latest {self.os_name}")
        recv_appdata = json.load(self.soc.recv(256).decode())

        filename = recv_appdata["name"]
        url = recv_appdata["url"]
        desc = recv_appdata["description"]

        url_data = requests.get(url).content
        with open(filename, mode="wb") as f:
            f.write(url_data)

        match self.os_name:
            case "Darwin":
                filename = "rm.command"
                data = f'rm {application_data.appname}.app'
            case "Windows":
                filename = "rm.bat"
                data = f':Repeat\ndel {application_data.appname}.exe\nif exist {application_data.appname}.exe goto Repeat\nstart /b "" cmd /c del "%~f0"&exit /b\npause'
        with open(filename, mode="w") as f:
            f.write(data)
