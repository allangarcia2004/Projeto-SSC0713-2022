# Projeto-SSC0713-2022

## Tutorial de Instalação

1. Clone este projeto através do `git`:

    `git clone https://github.com/allangarcia2004/Projeto-SSC0713-2022.git`

2. Entre na pasta do projeto:

    `cd Projeto-SSC0713-2022`

3. Crie um ambiente virtual para não interferir com as dependências de outros projetos:

    `python3 -m venv venv `

4. Ative o ambiente virtual:

    `source venv/bin/activate`

5. Instale as dependências do projeto:

    `pip install -r requirements.txt`

## Como executar

O programa principal, a ser executado, está no arquivo `main.py`, na pasta `src/`. Assim, estando na pasta do projeto com o ambiente virtual ativado, execute:

`python src/main.py`

Ao final de cada geração, será salvo um arquivo `population.backup`. Com ele, você poderá, em uma execução futura do programa, utilizar essa população para continuar o treino a partir desse ponto. Para utilizar esse arquivo, utilize o comando:

`python src/main.py --use-backup`

## Controle do programa

Por padrão, o programa executa na velocidade máxima que o computador puder processar. Caso queira limitar sua velocidade a 60 frames por segundo (padrão para ser jogado por humanos), pressione a tecla `K`. Pressione novamente para reverter.

Por padrão, o programa irá desenhar todos os frames na tela. Para parar o desenho e ter um leve ganho de desempenho, pressione a tecla `D`. Pressione novamente para reverter.

Para finalizar o programa, utilize a tecla `Q`.
