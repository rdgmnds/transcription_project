import openai
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from moviepy.editor import VideoFileClip
from pathlib import Path
import queue
import time
import pydub

# Forçar identificação da variável da API
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# Guardar os arquivos de video e audio dentro de variáveis na pasta 'temp'
PASTA_TEMP = Path(__file__).parent / 'temp'
PASTA_TEMP.mkdir(exist_ok=True)
ARQUIVO_AUDIO_TEMP = PASTA_TEMP / 'audio.mp3'
ARQUIVO_VIDEO_TEMP = PASTA_TEMP / 'video.mp4'

client = openai.OpenAI()

# Usar servidor do google para ser possível fazer o deploy do app
#@st.cache_data
#def get_ice_servers():
    #return [{'urls': ['stun.stun.l.google.com:19302']}]


def transcrever_audio():

    prompt_input = st.text_input('Digite aqui o seu prompt (opcional)', key='input_audio', placeholder="Aqui você pode corrigir possíveis erros na transcrição")
    file_audio = st.file_uploader('Adicione um arquivo de áudio .mp3', type=['mp3'])

    if not file_audio is None:

        with st.spinner('Gerando transcrição. Aguarde...'):
            transcricao = client.audio.transcriptions.create(
            model='whisper-1',
            language='pt',
            response_format='text',
            file=file_audio,
            prompt=prompt_input
        )
            st.success('Transcrição realizada!', icon="✔")
            st.markdown(transcricao)


def transcrever_video():

    prompt_input = st.text_input('Digite aqui o seu prompt (opcional)', key='input_video', placeholder="Aqui você pode corrigir possíveis erros na transcrição")
    file_video = st.file_uploader('Adicione um arquivo de video .mp4', type=['mp4'])

    if not file_video is None:

        with st.spinner('Gerando transcrição. Aguarde...'):
            with open(ARQUIVO_VIDEO_TEMP, mode='wb') as video_f:
                video_f.write(file_video.read())

            moviepy_video = VideoFileClip(str(ARQUIVO_VIDEO_TEMP))
            moviepy_video.audio.write_audiofile(str(ARQUIVO_AUDIO_TEMP))

            with open(ARQUIVO_AUDIO_TEMP, 'rb') as arquivo_audio:

                transcricao = client.audio.transcriptions.create(
                model='whisper-1',
                language='pt',
                response_format='text',
                file=file_video,
                prompt=prompt_input
                )

                st.success('Transcrição realizada!', icon="✔")
                st.markdown(transcricao)


def main():

    st.header('Transcreva seus arquivos de aúdio e video de forma rápida! 🔥')
    st.divider()
    st.markdown('#### Selecione a opção desejada e faça o upload do arquivo ✌')
    tab_video, tab_audio = st.tabs(['Video', 'Áudio'])

    with tab_audio:
        transcrever_audio()
    
    with tab_video:
        transcrever_video()

if __name__ == '__main__':
    main()