from flask import Flask, render_template, request, redirect, url_for
import yt_dlp
import logging

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Renderiza a página inicial onde o usuário insere o URL do vídeo.
    Ao enviar o formulário POST, redireciona para a rota 'options' com o URL do vídeo.
    """
    if request.method == 'POST':
        video_url = request.form['video_url']
        return redirect(url_for('options', video_url=video_url))
    return render_template('index.html')

@app.route('/options', methods=['GET', 'POST'])
def options():
    """
    Mostra as opções disponíveis para download do vídeo especificado pelo URL.
    Permite selecionar o formato desejado e iniciar o download.
    """
    video_url = request.args.get('video_url')
    app.logger.info(f"Received video URL: {video_url}")

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,  # Evita baixar playlists completas
        'progress_hooks': [my_hook],  # Atualizações de progresso do download
        'logger': app.logger,  # Utiliza o logger do Flask para mensagens de log
        'max_filesize': None,  # Remove o limite de tamanho de arquivo (em bytes)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])
            app.logger.info(f"Number of formats found: {len(formats)}")
    except Exception as e:
        app.logger.error(f"Error accessing video: {e}")
        return f"Erro ao acessar o vídeo: {e}"

    # Filtrar streams de áudio (mp3) e vídeo (mp4)
    streams = []
    for i, fmt in enumerate(formats):
        ext = fmt['ext']
        format_note = fmt.get('format_note', 'N/A')
        size = fmt.get('filesize', 'Desconhecido') // (1024 * 1024) if 'filesize' in fmt else 'Desconhecido'
        
        # Filtra apenas formatos mp4 e mp3 com tamanho conhecido
        if ext in ['mp4', 'mp3'] and format_note != 'N/A' and size != 'Desconhecido':
            streams.append((i, ext, format_note, size))

    if request.method == 'POST':
        choice = int(request.form['choice'])
        selected_format = formats[choice]

        ydl_opts['format'] = selected_format['format_id']
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            app.logger.info(f"Download completed: {selected_format['url']}")
            return "Download concluído!"
        except Exception as e:
            app.logger.error(f"Error during download: {e}")
            return f"Erro ao fazer download: {e}"

    return render_template('options.html', streams=streams, video_url=video_url)

# Função de progresso do download
def my_hook(d):
    """
    Função de progresso do download.
    Registra o progresso do download e exibe mensagens de log.
    """
    if d['status'] == 'finished':
        app.logger.info('Download completo!')
    elif d['status'] == 'downloading':
        app.logger.info(f"Baixando... {d['_percent_str']}")

if __name__ == '__main__':
    app.run(debug=True)
