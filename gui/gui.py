from pathlib import Path
import customtkinter as ctk
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
import re
import os


class YoutubeVideoDownloaderApp:
    def __init__(self, root, *args, **kwargs):
        self.root = root

        # Color Palette
        self.main_bg = '#00224D'
        self.primary_red = '#E71F2D'
        self.secondary_red = '#BE1520'

        self.root.configure(bg_color=self.main_bg)

        # Entry and Label Link Video
        self.link_label = ctk.CTkLabel(
            self.root, text="Link do vídeo:",
            font=("Roboto", 18))
        self.link_label.pack_configure(anchor='center', pady=(30, 0))

        self.var_entry = ctk.StringVar()
        self.entry_link = ctk.CTkEntry(
            self.root, border_color=self.primary_red, width=400, height=35,
            placeholder_text="www.youtube.com/...",
            textvariable=self.var_entry)
        self.entry_link.pack_configure(anchor='center', pady=(15, 0))

        # Type choice (áudio / vídeo) - Frame and Input
        self.type_file_label = ctk.CTkLabel(
            self.root, text="Selecione o tipo de arquivo",
            font=("Roboto", 18))
        self.type_file_label.pack_configure(
            anchor='center', pady=(30, 10))

        self.file_type_frame = ctk.CTkFrame(
            self.root, fg_color=self.secondary_red)
        self.file_type_frame.pack_configure(pady=(0))

        self.var_file_type = ctk.StringVar(value='video')
        self.type_choice_video = ctk.CTkRadioButton(
            self.file_type_frame, text='Vídeo', value='video',
            variable=self.var_file_type, command=self.layout_update)
        self.type_choice_video.pack_configure(
            side='left', padx=(50, 0), pady=5)

        self.type_choice_audio = ctk.CTkRadioButton(
            self.file_type_frame, text='Áudio', value='audio',
            variable=self.var_file_type, command=self.layout_update)
        self.type_choice_audio.pack_configure(
            side='left', pady=5)

        # Quality Frame and Label
        self.quality_label = ctk.CTkLabel(
            self.root, font=("Roboto", 18))
        self.quality_label.pack_configure(
            anchor='center', pady=(30, 10))

        self.quality_choice_frame = ctk.CTkFrame(
            self.root)
        self.quality_choice_frame.pack_configure(
            anchor='center', pady=(0, 0))

        # Download Button
        self.download_button = ctk.CTkButton(
            self.root, text="Baixar", fg_color=self.secondary_red,
            command=self.execute_download, height=35,
            font=("Roboto", 16),
            hover_color=self.primary_red)
        self.download_button.pack_configure(
            anchor='center', pady=(45, 0))

        # Output Information
        self.output_frame = ctk.CTkFrame(
            self.root)
        self.output_frame.pack_configure(
            anchor='center', pady=(30, 0))

        self.output_label = ctk.CTkLabel(
            self.output_frame, text='Aguardando seleção de vídeo do usuário',
            width=450, height=35)
        self.output_label.pack_configure(
            anchor='center')

        self.layout_update()

    def layout_update(self, *args):
        for widget in self.quality_choice_frame.winfo_children():
            widget.destroy()

        if self.var_file_type.get() == 'video':
            self.if_video_file()
        elif self.var_file_type.get() == 'audio':
            self.if_audio_file()

    def if_video_file(self, *args):
        self.quality_choice_frame.configure(fg_color=self.secondary_red)
        self.quality_label.configure(text="Selecione a qualidade do Vídeo")

        self.var_quality_res = ctk.StringVar(value='360p')
        resolutions = ['360p', '480p', '720p', '1080p']

        for res in resolutions:
            radio_button = ctk.CTkRadioButton(
                self.quality_choice_frame, text=res,
                variable=self.var_quality_res,
                value=res)
            radio_button.pack_configure(side='left', pady=5, padx=(20, 0))

    def if_audio_file(self, *args):
        self.quality_choice_frame.configure(fg_color=self.secondary_red)
        self.quality_label.configure(text="Selecione a qualidade do Áudio")

        self.var_quality_abr = ctk.StringVar(value='128kbps')
        bitrates = ['50kbps', '128kbps', '160kbps']

        for bit in bitrates:
            radio_button = ctk.CTkRadioButton(
                self.quality_choice_frame, text=bit,
                variable=self.var_quality_abr,
                value=bit)
            radio_button.pack_configure(side='left', pady=5, padx=(20, 0))

    def execute_download(self):
        self.output_label.configure(text='Verificando disponibilidade...')

        self.link_video = None
        try:
            self.link_video = YouTube(self.var_entry.get())
            self.video_title = (
                re.sub(r'[\\/*?:"<>|]', "", self.link_video.title))
            self.final_download_path = Path.home() / 'Downloads'
        except (RegexMatchError, VideoUnavailable):
            self.output_label.configure(text="Vídeo indisponível ou inválido")

        if self.link_video is None:
            self.output_label.configure(text="O campo de link está vazio")
            return

        if self.var_file_type.get() == 'video':
            self.download_video()
        elif self.var_file_type.get() == 'audio':
            self.download_audio()

    def download_video(self):
        self.video_streams = self.link_video.streams.filter(
            resolution=self.var_quality_res.get(), mime_type='video/mp4'
        ) or self.link_video.streams.filter(
            resolution=self.var_quality_res.get(), mime_type='video/webm'
        )
        self.audio_streams = self.link_video.streams.filter(
            abr='160kbps'
        ) or self.link_video.streams.filter(
            abr='128kbps'
        )

        if not self.video_streams:
            self.output_label.configure(text="Formato de vídeo não disponível")
            return

        download_path = 'temp_ffmpeg/'
        video_path = 'temp_ffmpeg/video.mp4'
        audio_path = 'temp_ffmpeg/audio.mp4'
        final_path = self.final_download_path / f"{self.video_title}.mp4"

        self.output_label.configure(text="Baixando vídeo...")
        self.video_streams.first().download(
            output_path=download_path, filename='video.mp4'
        )
        self.audio_streams.first().download(
            output_path=download_path, filename='audio.mp4'
        )

        command = (
                f'ffmpeg -i "{video_path}" -i "{audio_path}" '
                f'-c:v copy -c:a aac "{final_path}"')
        os.system(command)

        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

        self.output_label.configure(
            text='Download Concluído!'
        )

    def download_audio(self):
        self.audio_streams = self.link_video.streams.filter(
            abr=self.var_quality_abr.get()
        )

        self.audio_streams.first().download(
            output_path=self.final_download_path,
            filename=f'{self.video_title}.mp4'
        )
        self.output_label.configure(
            text='Download Concluído!'
        )


if __name__ == '__main__':
    root = ctk.CTk()
    root.geometry('450x450')
    app = YoutubeVideoDownloaderApp(root)
    root.mainloop()
