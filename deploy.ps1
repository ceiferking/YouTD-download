# Atualizar o código do repositório (supondo que você esteja usando Git)
git pull origin main

# Ativar o ambiente virtual
.\venv\Scripts\activate

# Instalar as dependências
pip install -r requirements.txt

# Parar o Nginx se estiver rodando
nginx -s stop

# Iniciar o Waitress
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "run.py"

# Iniciar o Nginx
start nginx
