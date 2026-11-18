"""Baixador de vídeos do TikTok e Instagram (HD, sem marca d'água quando possível).

Uso:
    pip install -r requirements.txt
    python app.py
    abrir http://localhost:5000
"""
import os
import re
import shutil
import tempfile
from urllib.parse import urlparse

from flask import Flask, jsonify, request, send_file, after_this_request
import yt_dlp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Só aceitamos links desses domínios (evita uso do servidor para outros fins)
ALLOWED_HOSTS = (
    "tiktok.com",
    "instagram.com",
    "instagr.am",
)


def host_permitido(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return False
    host = parsed.hostname.lower()
    return any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS)


def nome_seguro(texto: str) -> str:
    texto = re.sub(r"[^\w\- ]+", "", texto or "video", flags=re.UNICODE).strip()
    return (texto[:60] or "video").replace(" ", "_")


@app.route("/")
def index():
    return send_file(os.path.join(BASE_DIR, "index.html"))


@app.route("/api/baixar", methods=["POST"])
def baixar():
    dados = request.get_json(silent=True) or {}
    url = (dados.get("url") or "").strip()

    if not host_permitido(url):
        return jsonify(erro="Cole um link válido do TikTok ou do Instagram."), 400

    pasta = tempfile.mkdtemp(prefix="dl_")

    @after_this_request
    def limpar(resposta):
        shutil.rmtree(pasta, ignore_errors=True)
        return resposta

    opcoes = {
        "outtmpl": os.path.join(pasta, "%(id)s.%(ext)s"),
        # Melhor qualidade em mp4 já com áudio, evitando o formato "download"
        # do TikTok, que é o que vem com marca d'água.
        "format": "best[ext=mp4][format_id!*=download]/best[ext=mp4]/best",
        "format_sort": ["res", "br"],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 20,
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)
            caminho = ydl.prepare_filename(info)
    except yt_dlp.utils.DownloadError as e:
        msg = str(e)
        if "login" in msg.lower() or "private" in msg.lower():
            msg = "Esse vídeo é privado ou exige login. Só funciona com posts públicos."
        else:
            msg = "Não consegui baixar esse vídeo. Confira se o link está correto e é público."
        return jsonify(erro=msg), 422
    except Exception:
        return jsonify(erro="Erro inesperado ao baixar o vídeo."), 500

    if not os.path.exists(caminho):
        return jsonify(erro="O arquivo não foi gerado."), 500

    titulo = nome_seguro(info.get("title") or info.get("id"))
    ext = os.path.splitext(caminho)[1] or ".mp4"
    return send_file(caminho, as_attachment=True, download_name=f"{titulo}{ext}")


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
