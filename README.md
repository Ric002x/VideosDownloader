# 📥 Youtube Video Downloader

Este projeto é um software para baixar vídeos do Youtube, e que está atualmente **EM DESENVOLVIMENTO**. Nele, é permitido baixar o vídeo e audio em diferentes resoluções.


## 🔧 Funcionalidades

  - Download de vídeos em diferentes resoluções (360p, 480p, 720p, 1080p) - Atualmente
  - Download somente do áudio em diferentes bitrates


## 📋 Tecnologias E Bibliotecas Utilizadas

  - **Python 3.12.3**
    - **pytube**: Biblioteca que permite fazer os download de videos do Youtube.
    - **ffmpeg**: Programa que permite converter/criar stream de áudio e vídeo em diversos formatos.
    - **CustomTkinter 5.2.2**: Biblioteca baseada no Tkinter, que oferece uma estilização mais moderna e widgets totalmente customizáveis.


## 📦 Instalação

1. Clone o repositório em um diretório vazio:

```bash
git clone git@github.com:Ric002x/PortifolioPython.git
```

2. Crie um ambiente virtual (opcional):

 - criar ambiente:
```bash
python -m venv venv
```

 - ativar ambiente:

  - No macOS/Linux:
```bash
source venv/bin/activate  # Para Linux/Mac
```

  - No Windows:
```bash
.venv/Scripts/activate  # Para Windows
```

3. Instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```


## 🚀 Uso

O uso deste programa é bem simples. Após o seu início, basta colar o link do vídeo desejado, selecionar o tipo de arquivo desejado (audio ou vídeo), e selecionar a qualidade/resolução.

1. Execute o script:

  - "main.py"
```bash
python main.py
```

2. Cole o link do vídeo desejado:

  - www.youtube.com/...

3. Selecione o tipo de arquivo:

  - Áudio
  - Vídeo

4. Ao selecionar vídeo, o programa selecionará automaticamente a stream com melhor qualidade de áudio para efetuar o download. Já ao selecionar somente áudio, será possível escolher a qualidade de acordo com sua disponibilidade.

5. Após isso, o programa pedirá para digitar 'ok' para cofirmar o download. Ao confirmar, o arquivo baixado será mandado para o pasta de downloads do usuário. (Usuários Linux/Mac, o download ficará nas pasta raiz do programa)


## 🛠️ Implantação

### 📚 Biblioteca ffmpeg:

1 Devido a algumas streams de vídeo não serem acompanhadas de áudio, é necessário o uso da biblioteca ffmpeg que, quando o usuário selecionar a opção vídeo, o programa baixará também um arquivo de áudio, e ambos serão mesclados automaticamente utilizando-se do ffmpeg.

  - Para utilizá-lo, é necessário fazer o download em: [ffmpeg builds](https://www.gyan.dev/ffmpeg/builds/), mais precisamente, o arquivo: ffmpeg-release-essentials.7z, e então extrair em algum local de sua preferência. (É recomendado que o usuário coloque na pasta de arquivos de programas).

2 Após o download, atualize o PATH nas variáveis do ambiente para incluir o ffmpeg.

  - 'C:/Program Files/ffmpeg-7.0.1-essentials_build/bin'
![Variáveis de Ambiente](https://www.oobj.com.br/bc/assets/Articles/180/Screenshot_41.png)


## 📜 Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
