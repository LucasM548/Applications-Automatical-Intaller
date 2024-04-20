from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QMessageBox, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pathlib import Path
from tqdm import tqdm
import webbrowser
import subprocess
import requests
import winreg
import sys
import os

class AppInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Applications Automatical Intaller")
        def Store_url(productid):
            return f"ms-windows-store://pdp?hl=fr-fr&gl=fr&referrer=storeforweb&source=https%3A%2F%2Fwww.google.com%2F&productid={productid}&mode=mini&pos=7%2C2%2C1922%2C922"
        def extension_url(id):
            return f"https://chrome.google.com/webstore/detail/{id}"
        self.applications = {
            "Brave": {"url": "https://laptop-updates.brave.com/latest/winx64"},
            "Discord": {"url": "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64"},
            "Google Drive": {"url": "https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe"},
            "Epic Games": {"url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi"},
            "Git": {"url": "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe"},
            "GOG Galaxy": {"url": "https://webinstallers.gog-statics.com/download/GOG_Galaxy_2.0.exe?payload=aKB7F3BHw5NoN2YWknDMijQCYnKgHNmiuE-ZQH5qOFwqEprfTG4XR9vIgNeGZ1bBFQ2v7owOBlberSmn-yntUfS_14Aeqz3fwP2gAmbadgMcI9zO000XgA_7rXdfrzBTmnAGSLkOp9726xxtCKf8-OgkjdudGNIO_Rmgcjb5YEV2HwJV7kTft9jrTFD2haCI6Py8Sht6AiAMQKwcKU-pItTuypAjuSihxff5IcpeAqDeRyKQDF1cJlpe_D5hrDC5SLGykrIaXdP6ZjWTG9U0YDWYacADIeObsaiuTUbKEQU32bvfz0-p1v3JJYS20PFYSxccdCsavCo2K6E_eVAgKT1EsSVc96l_uxM4Sl2jxoYo4_5py65cKpSsv2osfCvu31LKZ6TvkRFZ8rm6MYeJx0OX5ASiiRAqmBCl2LYr6eFqnbmdyFb5mFNHVTvSTPHY5jt1HG3je2IOXdgtWMP8G7q7Gv-22JUF0q1QCjqPOxz-KClk-UDCKkgKZQVT4m0RB26q3McGHzUYUpHQThP1vA8A555MhyUevz5UHTinjzib8rtGHKn3_J1geGrYobhpy0yTOJ_UHE_pnUP-bxMYPRyJpKf-DNZbdvo99q_C47Jp38WD5fg4wgmJvjoWhI3KU04CabrE4Pl9VuXDFu4R5p8xLNSzp28QrG-G6nb6ZQ3YNZdrId4sOqlS-kNUhscX0eQzRRJoLc6ih5c3v24uoMks8OFhhhJzw2NgRlijgrR2cxgjsYXFYbu3OfMNXywyA3Ds"},
            "Java": {"url": "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=249553_4d245f941845490c91360409ecffb3b4"},
            "Logitech G HUB": {"url": "https://download01.logi.com/web/ftp/pub/techsupport/gaming/lghub_installer.exe"},
            "Modrinth": {"url": "https://launcher-files.modrinth.com/versions/0.6.3/windows/Modrinth%20App_0.6.3_x64_en-US.msi"},
            "Oculus": {"url": "https://www.oculus.com/download_app/?id=1582076955407037"},
            "Parsec": {"url": "https://s3.amazonaws.com/parsec-build/package/parsec-windows.exe"},
            "ProtonVPN": {"url": "https://protonvpn.com/download/ProtonVPN_v3.2.10.exe"},
            "Rockstar Games": {"url": "https://gamedownloads.rockstargames.com/public/installer/Rockstar-Games-Launcher.exe"},
            "Steam": {"url": "https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe"},
            "Streamlabs": {"url": "https://streamlabs.com/streamlabs-desktop/download?sdb=0"},
            "Wemod": {"url": "https://www.wemod.com/download/direct"},
            "Winrar": {"url": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-700fr.exe"},
            "Davinci Resolve (manual)": {"url": "https://www.blackmagicdesign.com/fr/products/davinciresolve"},
            "HWINFO (manual)": {"url": "https://www.hwinfo.com/download/"},
            "NVIDIA App (manual)": {"url": "https://fr.download.nvidia.com/nvapp/client/10.0.0.535/NVIDIA_app_beta_v10.0.0.535.exe"},
            "NVIDIA GeForce NOW (manual)": {"url": "https://download.nvidia.com/gfnpc/GeForceNOW-release.exe"},
            "Voicemod (manual)": {"url": "https://www.voicemod.net/"},
            "Authentificator": {"url": extension_url("authenticator/bhghoamapcdpbohphigoooaddinpkbai"), "type": "extension"},
            "Buster - Captcha Solver": {"url": extension_url("buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl/related"), "type": "extension"},
            "Dark Reader": {"url": extension_url("dark-reader/eimadpbcbfnmbkopoojfekhnkhdbieeh"), "type": "extension"},
            "Google Traduction": {"url": extension_url("google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb"), "type": "extension"},
            "Hower Zoom+": {"url": extension_url("hover-zoom%2B/pccckmaobkjjboncdfnnofkonhgpceea"), "type": "extension"},
            "Return YouTube Dislike": {"url": extension_url("return-youtube-dislike/gebbhagfogifgggkldgodflihgfeippi"), "type": "extension"},
            "SponsorBlock": {"url": extension_url("sponsorblock-for-youtube/mnjggcdmjocbbbhaepdhchncahnbgone"), "type": "extension"},
            "Steam Inventory Helper": {"url": extension_url("steam-inventory-helper/cmeakgjggjdlcpncigglobpjbkabhmjl"), "type": "extension"},
            "Twitch Live": {"url": extension_url("twitch-live-extension/nlnfdlcbnpafokhpjfffmoobbejpedgj"), "type": "extension"},
            "Volume Booster": {"url": extension_url("buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl"), "type": "extension"},
            "Visual Studio Code": {"url": Store_url("xp9khm4bk9fz7q"), "type": "microsoft"},
            "Microsoft PowerToys": {"url": Store_url("xp89dcgq3k6vld"), "type": "microsoft"},
            "Pichon": {"url": Store_url("9nk8t1kshffr"), "type": "microsoft"},
            "Wintoys": {"url": Store_url("9p8ltpgcbzxd"), "type": "microsoft"},
            "Office": {"url": Store_url("9wzdncrd29v9"), "type": "microsoft"},
        }
        self.setup_ui()

    #=================== UI ===================
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)

        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Applications", font=title_font), alignment=Qt.AlignCenter)
        title_layout.addWidget(QLabel("Chrome Extensions", font=title_font), alignment=Qt.AlignCenter)
        title_layout.addWidget(QLabel("Microsoft Store Applications", font=title_font), alignment=Qt.AlignCenter)
        layout.addLayout(title_layout)

        select_all_layout = QHBoxLayout()
        layout.addLayout(select_all_layout)

        column1 = QVBoxLayout()
        column2 = QVBoxLayout()
        column3 = QVBoxLayout()
        
        select_all_column1_button = QPushButton("All select")
        select_all_column1_button.clicked.connect(lambda: self.select_all_column(self.column1_checkboxes))
        select_all_layout.addWidget(select_all_column1_button)

        select_all_column2_button = QPushButton("All select")
        select_all_column2_button.clicked.connect(lambda: self.select_all_column(self.column2_checkboxes))
        select_all_layout.addWidget(select_all_column2_button)

        select_all_column3_button = QPushButton("All select")
        select_all_column3_button.clicked.connect(lambda: self.select_all_column(self.column3_checkboxes))
        select_all_layout.addWidget(select_all_column3_button)

        columns_layout = QHBoxLayout()
        layout.addLayout(columns_layout)

        columns_layout.addLayout(column1)
        columns_layout.addItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        columns_layout.addLayout(column2)
        columns_layout.addItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        columns_layout.addLayout(column3)
        columns_layout.addItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.checkboxes = {}
        self.column1_checkboxes = []
        self.column2_checkboxes = []
        self.column3_checkboxes = []

        for app, details in self.applications.items():
            app_type = self.get_application_type(details)
            checkbox = QCheckBox(app)
            if "manual" in app:
                checkbox.setStyleSheet("color: purple")
                column1.addWidget(checkbox)
                self.column1_checkboxes.append(checkbox)
            elif app_type == "extension":
                checkbox.setStyleSheet("color: green")
                column2.addWidget(checkbox)
                self.column2_checkboxes.append(checkbox)
            elif app_type == "microsoft":
                checkbox.setStyleSheet("color: blue")
                column3.addWidget(checkbox)
                self.column3_checkboxes.append(checkbox)
            else:
                column1.addWidget(checkbox)
                self.column1_checkboxes.append(checkbox)

            self.checkboxes[app] = checkbox

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        install_button = QPushButton("Install")
        install_button.clicked.connect(self.install_applications)
        button_layout.addWidget(install_button)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        button_layout.addWidget(quit_button)
    #================ END OF UI ================
    def select_all_column(self, column_checkboxes):
        if column_checkboxes[0].isChecked():
            for checkbox in column_checkboxes:
                checkbox.setChecked(False)
        else:
            for checkbox in column_checkboxes:
                checkbox.setChecked(True)

    #================================= INSTALLATION DES APPLICATIONS ================================
    def get_application_type(self, app_details):
        return app_details.get("type")
    
    def install_applications(self):
        applications_installed = [app for app, checkbox in self.checkboxes.items() if checkbox.isChecked()]
        if not applications_installed:
            QMessageBox.information(self, "Information", "No application selected!")
            return

        downloads_path = self.get_downloads_path()
        for app in applications_installed:
            details = self.applications[app]
            url = details["url"]
            app_type = self.get_application_type(details)
            try:
                if app_type in ['extension', 'microsoft'] or "(manual)" in app:
                    if app_type == "microsoft":
                        QMessageBox.information(self, "Information", f"Please manually install the {app} application from the Microsoft Store.")
                    webbrowser.open(url)
                else:
                    file_path = downloads_path / (f"{app}.msi" if url.endswith('.msi') else f"{app}.exe")

                    response = requests.get(url, stream=True)
                    total_size = int(response.headers.get('content-length', 0))
                    with open(file_path, "wb") as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=f'Downloading {app}', unit_divisor=1024) as pbar:
                        for data in response.iter_content(chunk_size=1024):
                            f.write(data)
                            pbar.update(len(data))

                    if url.endswith('.msi'):
                        subprocess.Popen(["msiexec", "/i", str(file_path)], shell=True)
                    else:
                        subprocess.Popen([str(file_path)], shell=True)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Unable to install {app} : {str(e)}")
        self.close()
    #============================= END OF INSTALLATION DES APPLICATIONS ==============================

    #================================= CHEMIN DE TELECHARGEMENT ================================
    def get_downloads_path(self):
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                value, _ = winreg.QueryValueEx(key, downloads_guid)
                downloads_path = os.path.expandvars(value)
                return Path(downloads_path)
        except FileNotFoundError:
            return Path.home() / "Downloads"
    #============================= END OF CHEMIN DE TELECHARGEMENT ==============================

if __name__ == '__main__':
    app = QApplication(sys.argv)
    installer = AppInstaller()
    installer.show()
    sys.exit(app.exec_())