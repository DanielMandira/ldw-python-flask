### Criando ambiente virtual: 
* python -m venv venv

### Alterando privilégios no PowerShell (se necessário):
> Execute o PowerShell como Administrador e rode o seguinte comando:
* Set-ExecutionPolicy RemoteSigned

### Ativando o ambiente virtual:
* venv\Scripts\activate

### Desativando o ambiente virtual:
* deactivate

### Gerando a lista de dependências:
* pip freeze > requirements.txt

### Instalando pacotes a partir da lista de dependências:
* pip install -r requirements.txt
