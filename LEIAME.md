# Baixador de vídeos TikTok e Instagram

Site simples: você cola o link do vídeo, clica em **Baixar** e recebe o arquivo em HD, sem marca d'água.

## Arquivos

- `app.py`: servidor (Flask + yt-dlp) que baixa o vídeo
- `index.html`: a página do site
- `requirements.txt`: dependências

## Rodar no seu computador

1. Instale o Python 3.9 ou mais novo.
2. No terminal, dentro desta pasta:

   ```
   pip install -r requirements.txt
   python app.py
   ```

3. Abra http://localhost:5000 no navegador.

(Opcional) Instale o **ffmpeg** no computador: ajuda o yt-dlp com alguns vídeos do Instagram.

## Colocar online (para usar pelo celular, de qualquer lugar)

O site precisa de um servidor, então não funciona em hospedagem só de páginas (GitHub Pages, Netlify estático etc.).
Opções simples que rodam Python:

- **Render** ou **Railway**: crie um serviço web a partir deste projeto
  - Comando de build: `pip install -r requirements.txt`
  - Comando de start: `gunicorn app:app`
- Um VPS pequeno com `gunicorn app:app`

## Observações

- Só funciona com posts **públicos**. Vídeos privados ou que exigem login falham.
- TikTok e Instagram mudam as coisas com frequência. Se parar de funcionar, atualize o yt-dlp:
  `pip install -U yt-dlp`
- Sobre a marca d'água do TikTok: o programa pede a versão sem marca. Se o TikTok só entregar a versão com marca para algum vídeo específico, ele baixa o que estiver disponível.
- Instagram não coloca marca d'água no vídeo original, então o download já vem limpo.
- Use só para conteúdo seu ou com permissão do autor. Redistribuir vídeo de outras pessoas pode violar direitos autorais e os termos das plataformas.
- Se for deixar o site aberto para outras pessoas, considere limitar o número de downloads por IP para o servidor não ser abusado.
