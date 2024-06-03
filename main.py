import os, sys
import cv2
from PIL import Image
from kivy.resources import resource_add_path, resource_find
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from matplotlib import pyplot as plt
from os.path import basename
from os.path import splitext
from functions import *
from plyer import filechooser
import time


Window.size = (900, 600)
    
class MenuUtama(Screen):
    pass

class MenuEnkripsi(Screen):
    def on_leave(self):
        self.ids.selected_path.text = ""
        self.ids.key_a.text = ""
        self.ids.key_b.text = ""
        self.ids.process_time.text = ""
        self.ids.img.source = "images\gambar_kosong.png"  
        self.ids.img_encrypted.source = "images\enkripsi.png"  

class MenuDekripsi(Screen):
    def on_leave(self):
        self.ids.selected_path.text = ""  
        self.ids.key_a.text = ""
        self.ids.key_b.text = ""
        self.ids.process_time.text = ""
        self.ids.img.source = "images\gambar_kosong.png"
        self.ids.img_decrypted.source = "images\dekripsi.png"  

class BantuanPengguna(Screen):
    pass

class TentangAplikasi(Screen):
    pass

class MenuHisto(Screen):
   pass

class MenuRgb(Screen):
    def on_leave(self):
        self.ids.gambar_utm.source = "images/gambar_kosong.png"
        self.ids.selected_path_utm.text = "Lokasi : " 
        self.ids.histo.source = "images/histogram.png"
        self.ids.gambar_red.source = "images/histogram.png"
        self.ids.gambar_green.source = "images/histogram.png"
        self.ids.gambar_blue.source = "images/histogram.png"


class MenuAbu(Screen):
    def on_leave(self):
        self.ids.gambar_utm.source = "images/gambar_kosong.png"
        self.ids.selected_path_utm.text = "Lokasi : " 
        self.ids.abu.source = "images/histogram.png"
        self.ids.histoabu.source = "images/histogram.png"

class MyApp(MDApp):
    dialog = None

    def build(self):

        self.theme_cls.primary_palette = "Red"
        self.theme_cls.secondary_palette = "Black"
        self.theme_cls.theme_style = "Dark"

        Builder.load_file('interface.kv')

        screen_manager = ScreenManager()
        screen_manager.add_widget(MenuUtama(name='menuutama'))
        screen_manager.add_widget(MenuEnkripsi(name='enkripsi'))
        screen_manager.add_widget(MenuDekripsi(name='dekripsi'))
        screen_manager.add_widget(BantuanPengguna(name='bantuan'))
        screen_manager.add_widget(MenuHisto(name='menuhisto'))
        screen_manager.add_widget(MenuRgb(name='menurgb'))
        screen_manager.add_widget(MenuAbu(name='menuabu'))
        return screen_manager
    
    def goto_main_menu(self, *args):
        screen_manager = self.root
        screen_manager.transition = SlideTransition(direction='right')
        screen_manager.current = 'menuutama'

    def goto_info(self, *args):
        screen_manager = self.root
        screen_manager.transition = SlideTransition(direction='left')
        screen_manager.current = 'tentang'
    
    def current_slide(self, index):
        pass

    def file_chooser(self, btn_id):
        file_types = [("Image files", "*.bmp;*.jpg;*.png")]
        filechooser.open_file(on_selection=lambda x: self.selected(x, btn_id), filters=file_types)
        
    def selected(self, selection, btn_id):
        if selection:
            current_screen = self.root.current_screen
            if btn_id == 'img':
                    current_screen.ids.img.source = selection[0]
                    current_screen.ids.selected_path.text = selection[0]
            elif btn_id == 'gambar_utm':
                    current_screen.ids.gambar_utm.source = selection[0]
                    current_screen.ids.selected_path_utm.text = selection[0]
            
            
    def btn_enkripsi(self):
        try:
            current_screen = self.root.current_screen
            key_a = float(current_screen.ids.key_a.text)
            key_b = float(current_screen.ids.key_b.text)
            key_value = (key_a, key_b)
            print(key_value)
            image_path = current_screen.ids.selected_path.text

            if current_screen.ids.img.source == "gambar_kosong.png":
                return
            
            if image_path:
                start_time = time.time()
                HenonEncryption(image_path, key_value)
                end_time = time.time()
                time_difference = end_time - start_time
                rounded_time = round(time_difference, 5)
                process_time = f"Waktu : {rounded_time} detik"
                encrypted_path = image_path.split('.')[0] + "_HenonEnc.png"
                result_path = str(encrypted_path)
                current_screen.ids.process_time.text = process_time
                current_screen.ids.img_encrypted.source = encrypted_path
                current_screen.ids.result_path.text = result_path

            self.show_alert_dialog(f"Enkripsi Citra Berhasil!","")

        except :
            self.show_alert_dialog("Enkripsi Citra Gagal","Periksa kembali inputan anda!")

    def btn_dekripsi(self):
        try:
            current_screen = self.root.current_screen
            key_a = float(current_screen.ids.key_a.text)
            key_b = float(current_screen.ids.key_b.text)
            key_value = (key_a, key_b)
            image_path = current_screen.ids.selected_path.text

            if current_screen.ids.img.source == "gambar_kosong.png":
                return
            
            if image_path:
                start_time = time.time()
                HenonDecryption(image_path, key_value)
                end_time = time.time()
                time_difference = end_time - start_time
                rounded_time = round(time_difference, 5)
                process_time = f"Waktu : {rounded_time} detik"
                decrypted_path = image_path.replace('_HenonEnc', '_HenonDec')
                result_path = str(decrypted_path)
                current_screen.ids.process_time.text = process_time
                current_screen.ids.img_decrypted.source = decrypted_path
                current_screen.ids.result_path.text = result_path

            self.show_alert_dialog(f"Dekripsi Citra Berhasil!","")
        
        except :
            # Tangani kesalahan di sini, misalnya tampilkan pesan kesalahan
            self.show_alert_dialog("Dekripsi Citra Gagal","Periksa kembali inputan anda!")


    def btn_rgb(self):
        try:
            current_screen = self.root.current_screen
            if current_screen.ids.gambar_utm.source == "images/gambar_kosong.png":
                self.show_alert_dialog("Pilih citra terlebih dahulu!", "")
                return
            image_path_a = current_screen.ids.gambar_utm.source
            image_name_a = os.path.basename(image_path_a).split('.')[0]
            save_path = 'images/histogram/'          

            gambar_red, gambar_green, gambar_blue = self.tampil_histogram(image_path_a)     
             
            self.histogram(gambar_red, 'red', 'Red', image_name_a, save_path,)
            self.histogram(gambar_green, 'green', 'Green', image_name_a, save_path)
            self.histogram(gambar_blue, 'blue', 'Blue', image_name_a, save_path)


            current_screen.ids.gambar_red.source = f"{save_path}{image_name_a}_red_histogram.png"
            current_screen.ids.gambar_green.source = f"{save_path}{image_name_a}_green_histogram.png"
            current_screen.ids.gambar_blue.source = f"{save_path}{image_name_a}_blue_histogram.png"

            self.plot_rgb_histogram(gambar_red, gambar_green, gambar_blue, image_name_a, save_path)
            current_screen.ids.histo.source = f"{save_path}{image_name_a}_histogram_rgb.png"
        except Exception as e:
            self.show_alert_dialog("Gagal!", "Periksa kembali inputan anda!")

    def tampil_histogram(self, file_path):
        img = cv2.imread(file_path)
        r_channel, g_channel, b_channel = cv2.split(img)
        gambar_red = cv2.calcHist([r_channel], [0], None, [256], [0, 256])  
        gambar_green = cv2.calcHist([g_channel], [0], None, [256], [0, 256])
        gambar_blue = cv2.calcHist([b_channel], [0], None, [256], [0, 256])
        gambar_red = np.squeeze(gambar_red)
        gambar_green = np.squeeze(gambar_green)
        gambar_blue = np.squeeze(gambar_blue)
        return gambar_red, gambar_green, gambar_blue
        
    def histogram(self, hist, color, channel_name, image_name, save_path):
        print("Plotting histogram for:", image_name, channel_name)
        plt.plot(hist, color=color, label=channel_name)
        plt.xlabel('Pixel Values')
        plt.ylabel('Pixel Count')
        plt.title(f'{channel_name} Histogram')
        plt.legend()
        histogram_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
        os.makedirs(histogram_folder, exist_ok=True)
        histogram_filename = f"{image_name}_{channel_name.lower()}_histogram.png"
        histogram_path = os.path.join(histogram_folder, histogram_filename)
        plt.savefig(histogram_path)
        plt.close()

        

    def plot_rgb_histogram(self, gambar_red, gambar_green, gambar_blue, image_name, save_path):
        plt.plot(gambar_red, color='red', label='Red')
        plt.plot(gambar_green, color='green', label='Green')
        plt.plot(gambar_blue, color='blue', label='Blue')
        plt.xlabel('Pixel Values', fontsize=16)
        plt.ylabel('Pixel Count', fontsize=16)
        plt.title(f'RGB Histogram', fontsize=16)
        plt.legend()
        histogram_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
        os.makedirs(histogram_folder, exist_ok=True)
        histogram_filename = f"{image_name}_histogram_rgb.png"
        histogram_path = os.path.join(histogram_folder, histogram_filename)
        plt.savefig(histogram_path)
        plt.close()

    def btn_abu(self):
        try:
            current_screen = self.root.current_screen
            if current_screen.ids.gambar_utm.source == "images/gambar_kosong.png":
                self.show_alert_dialog("Pilih citra terlebih dahulu!", "")
                return
            image_path_a = current_screen.ids.gambar_utm.source
            image_name_a = os.path.basename(image_path_a).split('.')[0]
            save_path = 'images/grayscale/'             

            self.proses_abu(image_path_a, save_path)
            
            current_screen.ids.histoabu.source = f"{save_path}{image_name_a}_histogram_grayscale.png"
        except Exception as e:
            self.show_alert_dialog("Gagal!", "Periksa kembali inputan anda!")

    def proses_abu(self, image_path, save_path) :
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # konversi RGB ke Grayscale menggunakan library OpenCV
        image_name = os.path.splitext(os.path.basename(image_path))[0]  # Mengambil nama gambar tanpa ekstensi
       
              
        histogram_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
        os.makedirs(histogram_folder, exist_ok=True)

        
        histogram_filename = f"{image_name}_histogram_grayscale.png"
        histogram_path = os.path.join(histogram_folder, histogram_filename)

        plt.hist(gray.ravel(), 256, [0, 256])  # Plot histogram gambar Grayscale
        plt.title('Histogram Grayscale')
        plt.xlabel('Intensitas Piksel')
        plt.ylabel('Jumlah Piksel')
        plt.savefig(histogram_path)
        plt.close()
        
        print("img path : ", image_path)
        print("save path : ", save_path)


        


      

    def show_alert_dialog(self, message, caption):
        if not self.dialog:
            self.dialog = MDDialog(
                title=message,
                text=caption,
                buttons=[
                    MDFlatButton(
                        text="OKE",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.dismiss_dialog,
                    ),
                ],
            )
        self.dialog.open()
    
    def dismiss_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()


if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = MyApp()
        app.run()
    except Exception as e:
        print(e)
        input("Press enter.")