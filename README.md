# ❤️ Conversor Word ⇄ PDF

Ferramenta gratuita e compatível com AdSense para converter arquivos Word (.doc, .docx) para PDF e vice-versa.

## Funcionalidades
- Conversão Word ⇄ PDF real com CloudConvert API
- Blocos reservados para anúncios
- SEO e Google Analytics
- Ícone ❤️

## Como usar localmente
1. Instale dependências:
```
pip install -r requirements.txt
```
2. Obtenha uma chave em https://cloudconvert.com/api/v2/keys
3. No terminal:
```
export CLOUDCONVERT_API_KEY=sua_chave
python server.py
```

## Como implantar no Render
- Crie um Web Service em Python
- Use:
  - Build command: `pip install -r requirements.txt`
  - Start command: `python server.py`
  - Environment Variable: `CLOUDCONVERT_API_KEY=sua_chave`

## Licença
MIT
