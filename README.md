📷 Processamento de Imagens com Ruídos

Este projeto aplica diferentes tipos de ruído em imagens, como:

-   Gaussian Noise
-   Salt and Pepper Noise
-   Uniform Noise

Além disso, exibe os resultados em uma interface gráfica.

------------------------------------------------------------------------

🚀 Como executar

1. Instalar as dependências

Antes de executar o programa, instale todas as bibliotecas necessárias
usando o arquivo dependences.txt:

pip install -r dependences.txt ou pip3 install -r dependences.txt

------------------------------------------------------------------------

2. Executar o programa via terminal

Após instalar as dependências, execute o programa com o comando:

python trabalho.py ou python trabalho.py

Isso abrirá a interface gráfica do sistema.

------------------------------------------------------------------------

3. Gerar o executável (.exe)

Caso queira distribuir o programa sem precisar instalar Python, você
pode gerar um executável usando o PyInstaller.

3.1 Instalar o PyInstaller

pip install pyinstaller ou pip3 install pyinstaller

------------------------------------------------------------------------

3.2 Gerar o executável

Execute o seguinte comando na pasta do projeto:

pyinstaller –onefile –windowed trabalho.py

------------------------------------------------------------------------

3.3 Localizar o executável

Após o processo, o arquivo será gerado em:

dist/trabalho.exe

------------------------------------------------------------------------

4. Executar o programa (.exe)

Para executar o programa compilado:

1.  Acesse a pasta dist
2.  Dê um duplo clique em:

trabalho.exe

Ou execute pelo terminal:

dist.exe

------------------------------------------------------------------------

⚠️ Observações

-   Certifique-se de que o arquivo dependences.txt está atualizado com
    todas as bibliotecas necessárias.
-   Caso utilize imagens externas, mantenha-as na mesma estrutura de
    pastas do projeto.
-   O executável pode demorar alguns segundos para abrir na primeira
    execução.

------------------------------------------------------------------------

📁 Estrutura do Projeto

projeto/

├── trabalho.py ├── dependences.txt ├── imagens/ └── README.txt

------------------------------------------------------------------------

👨‍💻 Autor

Projeto desenvolvido para estudo de processamento de imagens.
