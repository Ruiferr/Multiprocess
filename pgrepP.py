import os, time
import subprocess
from multiprocessing import Process, Value, Queue
from sys import argv
import logging

script = argv

## Verifica se a sintax do comando está correta.
try:
    assert len(script)>3
    if script[1]=='-p':
        assert int(script[2])
        nprocess=int(script[2])
    else:
        nprocess=1
except AssertionError:
    logging.error(' Sintax Incorreta. Consulte README.txt para obter ajuda.')
    exit(1)

word=script[-1] #Palavra/expressão que será procurada

fila_ficheiros=Queue()  
## Adiciona o nome dos ficheiros na fila
if script[3]==script[-1] and script[1]=='-p': # Verifica se foi inserido o nome de algum ficheiro.
    Parar=False
    while not Parar:        
        file=input('Insira o nome de um ficheiro ou a letra "Q" para terminar): ')
        if file=='Q' or file=='q':
            Parar=True
        else:
            fila_ficheiros.put(file)
else:
    if script[1]=='-p':
        index=3
    else:
        index=1
    for file_name in range(index,len(script)-1):
        fila_ficheiros.put(script[file_name])   

# Verifica se o número de processos é <= ao de ficheiros, caso contrário, para o programa.
try:
    assert nprocess<=fila_ficheiros.qsize() and nprocess>0
except AssertionError:
    logging.error(' O número de processos deve ser > 0 e <= o número de ficheiros.')
    exit(1)

#Número total de linhas encontradas nos ficheiros
global_counter=Value("i",0)
  
def exec_grep():  
    """
    Corre o comando 'grep' e procura a expressão inserida pelo utilizador.

    Ensures: A procura e impresão de todos os resultados encontrados correspondentes à expressão inserida.
    """ 
    while fila_ficheiros.qsize()!=0:  

        file=fila_ficheiros.get()
        
        proc = subprocess.run(["grep", word, file], universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        resultado="Processo PID "+str(os.getpid())+" processou "+file+"\n"

        if len(proc.stderr.splitlines())!=0: # Verifica se existe alguma exceção
            resultado=resultado+"> Erro: Ficheiro não encontrado!!!"+"\n"
        elif len(proc.stdout.splitlines())==0:
            resultado=resultado+"> Nenhuma correspondência."
        else:
            resultado=resultado+"Linhas encontradas:\n"
            for line in proc.stdout.splitlines():
                resultado=resultado+"> "+str(line)+"\n"   

        global_counter.value+=len(proc.stdout.splitlines())
        print(resultado)

Processos=[]
for file in range(nprocess):     
    Processos.append(Process(target=exec_grep))
    
for filho in Processos:
    filho.start()
    
for filho in Processos:
    filho.join()  


print("\nO processo Pai PID",str(os.getpid()),"informa que foram encontradas",global_counter.value,"linhas.",)
   


