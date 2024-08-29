from pytube import YouTube
import time
import os
import re
from pytube.exceptions import RegexMatchError, VideoUnavailable


class YoutubeVideoDownloader:
    def __init__(self, *args, **kwargs):
        self.get_youtube_video_link()
        self.get_stream_type()
        self.get_stream_quality()
        self.video_title = self.sanitize_filename(self.link_video.title)
        self.download_selected_stream()

    def get_youtube_video_link(self):
        print('\nPara fazer o download do vídeo desejado cole'
              ' abaixo o link do vídeo:\n')

        try:
            self.link_video = input()
            self.link_video = YouTube(self.link_video)
        except RegexMatchError:
            raise ValueError("Inisira um link válido")
        except VideoUnavailable:
            raise ValueError("O vídeo não está disponível")

        print('Você deseja baixar...')
        for i in range(3):
            time.sleep(0.6)
            print('.')
        self.video_title = self.link_video.title
        print(self.video_title)

        self.list_videos_streams = self.link_video.streams.filter(
            type='video',
            )

        self.list_audios_streams = self.link_video.streams.filter(
            type='audio',
            )

    def get_stream_type(self):
        while True:
            print('Selecione:\n  1: para baixar'
                  ' em formato de vídeo\n  2: para baixar em formato de áudio')
            try:
                self.cliente_type_choice = input()

                if self.cliente_type_choice == '1':
                    self.cliente_type_choice = 'video'
                elif self.cliente_type_choice == '2':
                    self.cliente_type_choice = 'audio'
                else:
                    raise ValueError(
                        '\nSelecione um valor válido!\n'
                    )
                print(self.cliente_type_choice)
                return self.cliente_type_choice
            except ValueError as err:
                print(err)

    def get_stream_quality(self):
        if self.cliente_type_choice == 'video':
            while True:
                try:
                    print('\nAgora selecione a qualidade de vídeo'
                          ' desejada. Digite:'
                          '\n  1: 360p'
                          '\n  2: 480p'
                          '\n  3: 720p'
                          '\n  4: 1080p'
                          )

                    self.cliente_quality_choice = input()

                    quality_mapping = {
                        '1': '360p',
                        '2': '480p',
                        '3': '720p',
                        '4': '1080p'
                    }

                    selected_quality = (
                        quality_mapping[self.cliente_quality_choice])

                    if not selected_quality:
                        raise ValueError(
                            '\nSelecione um valor válido\n'
                        )

                    # Get Video
                    if self.link_video.streams.filter(
                        resolution=selected_quality, mime_type='video/mp4'
                    ):
                        self.video_file = self.link_video.streams.filter(
                            resolution=selected_quality, mime_type='video/mp4'
                        )
                    elif self.link_video.streams.filter(
                        resolution=selected_quality, mime_type='video/webm'
                    ):
                        self.video_file = self.link_video.streams.filter(
                            resolution=selected_quality, mime_type='video/webm'
                        )
                    else:
                        print('Qualidade indispoível,'
                              ' por favor, selecione outra')
                        self.get_stream_quality()

                    # Get Audio
                    self.audio_file = self.link_video.streams.filter(
                        abr='160kbps',
                    ) or self.link_video.streams.filter(
                        abr='128kbps'
                    )

                    print(self.video_file)
                    print(self.audio_file)

                    return self.video_file

                except ValueError as err:
                    print(err)

        if self.cliente_type_choice == 'audio':
            print('\nNa Selecão de áudio, é priorizado a seleção'
                  ' daquele com maior qualidade')
            if self.list_audios_streams.filter(abr='160kbps'):
                self.audio_file = self.list_audios_streams.filter(
                    abr='160kbps'
                )
            elif self.list_audios_streams.filter(abr='128kbps'):
                self.audio_file = self.list_audios_streams.filter(
                    abr='128kbps'
                )
            else:
                self.audio_file = self.list_audios_streams
            print(self.audio_file)

    def sanitize_filename(self, filename):
        # Remove caracteres inválidos do nome do arquivo
        return re.sub(r'[\\/*?:"<>|]', "", filename)

    def get_download_path(self):
        # Obtém o caminho da pasta de Downloads do usuário
        if os.name == 'nt':  # Se for Windows
            download_path = os.path.join(
                os.environ['USERPROFILE'], 'Downloads')
        else:
            # Para sistemas Unix-like (Linux, MacOS), você pode
            # definir um caminho diferente
            download_path = os.path.join(
                os.path.expanduser('~'), 'Downloads')
        return download_path

    def download_selected_stream(self):
        if self.cliente_type_choice == 'video':
            iniciar = ''
            while iniciar != 'ok':
                iniciar = input('Digite ok para iniciar o download: ')

            video_title = self.video_title
            download_path = 'temp_ffmpeg/'
            final_download_path = self.get_download_path()
            output_path = os.path.join(
                final_download_path, f'{video_title}.mp4')

            self.video_file.first().download(
                output_path=download_path, filename='video.mp4')
            self.audio_file.first().download(
                output_path=download_path, filename='audio.mp4')

            video_path = 'temp_ffmpeg/video.mp4'
            audio_path = 'temp_ffmpeg/audio.mp4'

            command = (
                f'ffmpeg -i "{video_path}" -i "{audio_path}" '
                f'-c:v copy -c:a aac "{output_path}"')

            os.system(command)

            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)

        elif self.cliente_type_choice == 'audio':
            iniciar = ''
            while iniciar != 'ok':
                iniciar = input('Digite "ok" para iniciar o download:\n')

            video_title = self.video_title
            final_download_path = self.get_download_path()
            filename = f'{video_title}.mp4'

            self.audio_file.first().download(
                output_path=final_download_path, filename=filename)

        for i in range(3):
            time.sleep(0.3)
            print('.')
        print('Download Concluído!')


if __name__ == '__main__':
    YoutubeVideoDownloader()
