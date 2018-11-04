import os, time
import subprocess
from queue import Queue
from threading import Thread, currentThread
from sys import argv
import logging

script = argv

## Verifica se a sintax do comando está correta.
try:
    assert len(script)>3
    if script[1]=='-p':
        assert int(script[2])
        nthreads=int(script[2])
    else:
        nthreads=1
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
    assert nthreads<=fila_ficheiros.qsize() and nthreads>0
except AssertionError:
    logging.error(' O número de processos deve ser > 0 e <= o número de ficheiros.')
    exit(1)

#Número total de linhas encontradas nos ficheiros
global_counter=0
  
def exec_grep():  
    """
    Corre o comando 'grep' e procura a expressão inserida pelo utilizador.

    Ensures: A procura e impresão de todos os resultados encontrados correspondentes à expressão inserida.
    """ 
    global global_counter
    while fila_ficheiros.qsize()!=0:  

        file=fila_ficheiros.get()
        
        proc = subprocess.run(["grep", word, file], universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        resultado=currentThread().getName()+" processou "+file+"\n"

        if len(proc.stderr.splitlines())!=0: # Verifica se existe alguma exceção
            resultado=resultado+"> Erro: Ficheiro não encontrado!!!"+"\n"
        elif len(proc.stdout.splitlines())==0:
            resultado=resultado+"> Nenhuma correspondência."
        else:
            resultado=resultado+"Linhas encontradas:\n"
            for line in proc.stdout.splitlines():
                resultado=resultado+"> "+str(line)+"\n"   

        global_counter+=len(proc.stdout.splitlines())
        print(resultado)

Threads=[]
for file in range(nthreads):     
    Threads.append(Thread(name='Thread '+str(file+1),target=exec_grep))
    
for filho in Threads:
    filho.start()
    
for filho in Threads:
    filho.join()  

print("\nO processo Pai PID",str(os.getpid()),"informa que foram encontradas",global_counter,"linhas.",)
   


