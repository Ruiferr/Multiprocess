import os, time
import subprocess
from multiprocessing import Process, Value, Array, Queue
from sys import argv

script = argv

#Palavra que pretende buscar
word=script[-1]

start=time.time()

fila_ficheiros=Queue()    
for arg in range(3,len(script)-1):
    fila_ficheiros.put(script[arg])   

global_counter=Value("i",0)
proccess_counter=Value("i",0)



def exec_grep():  
    file=fila_ficheiros.get()
    proccess_counter.value+=1
    resultado="\nProcesso "+str(proccess_counter.value)+" - Filho: "+str(os.getpid())+"\n"
    proc = subprocess.run(["grep", word, file], universal_newlines = True, stdout=subprocess.PIPE)

    for line in proc.stdout.splitlines():
        resultado=resultado+str(line)+"\n"

    # Soma o número total de linhas do ficheiro
    global_counter.value+=len(proc.stdout.splitlines())
    print(resultado)

    time.sleep(1)

#-----------------------------------------------------

Processos=[]
for file in range(2):
    Processos.append(Process(target=exec_grep))
    
for filho in Processos:
    filho.start()
    #print(">>>> start")
    #time.sleep(1)
    
for filho in Processos:
    filho.join()  
    #print(">>>> Join")
#-----------------------------------------------------    
end=time.time()

print("Tempo = ",round(end-start,2), "segundos")

print("\nTotal de Linhas é",global_counter.value,".","PID Pai:",str(os.getpid()))
   
    
#Comando de Teste:
#python3 pgrep.py -p 2 fich1.txt fich2.txt export

#pthread
#Usar o numero de processos do stin
#Ter em atenção ao numero de processos/numero de ficheiros (criação de um processo para ler ficheiro que não existe)
#Nomes de ficheiros errados
#Ficheiros em branco

