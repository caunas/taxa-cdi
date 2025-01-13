## Sobre:

O programa consiste em consultar o valor da taxa CDI ao longos dos anos através da api do banco central, exportar em um arquivo csv e gerar um gráfico com os dados exportados. O usuário pode escolher o nome do arquivo do gráfico

## Pré-requisitos
É necessário ter o python (recomendada a versáo 3.11), o git, e o pip instalados na máquina

### Windows
Para instalar o git e o python, use o winget

1. Instalando git
``` powershell
winget install -e --id Git.Git
```

2. Instalando o python
``` powershell
winget install -e --id Python.Python.3.11
```
* Provável que o pip já venha instalado, mas caso contrário, você vai precisar fazer isso manualmente

* Para instalar o pip, baixe o arquivo de instalação clicando [aqui](https://bootstrap.pypa.io/get-pip.py), em seguida, execute-o

* ``` powershell
  python get-pip.py
  ```

Por ultimo, vamos verificar a instalação
``` powershell
#python
python --version

#git
git --version

#pip
pip --version
```
### Linux
``` bash
sudo apt install python3.11
```
``` bash
sudo apt install git
```
* Caso o pip não venha instalado, você vai precisar fazer isso
```
sudo apt install python3-pip
```

Depois de completar todos os passos, verifique se está tudo instalado
``` bash
# python
python3 --version

#git
git --version

#pip
pip3 --version
```
## Build
1. Clone o repositório
```
git clone https://github.com/caunas/automatic-invention
cd automatic-invention
```
2. Instale as dependências
```
pip install -r requirements.txt
```
3. Rode o arquivo principal
```
python main.py <nome_do_grafico>
```