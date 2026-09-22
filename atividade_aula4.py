import csv
import time
from datetime import datetime
import psutil

class Metrica:
    def __init__(self, nome: str, unidade: str):
        self.nome = nome
        self.unidade = unidade
        self.valor = 0.0

    def coletar(self):
        """Método genérico que será sobrescrito pelas classes filhas."""
        pass

class CpuMetrica(Metrica):
    def __init__(self):
        super().__init__(nome="CPU", unidade="%")

    def coletar(self):
        # Retorna o uso de CPU em porcentagem
        self.valor = psutil.cpu_percent(interval=1)
        return self.valor


class MemoriaMetrica(Metrica):
    def __init__(self):
        super().__init__(nome="Memoria", unidade="MB")

    def coletar(self):
        # Converte a memória usada de bytes para Megabytes (MB)
        memoria_bytes = psutil.virtual_memory().used
        self.valor = round(memoria_bytes / (1024 * 1024), 2)
        return self.valor


class DiscoMetrica(Metrica):
    def __init__(self):
        super().__init__(nome="Disco", unidade="MB")

    def coletar(self):
        # Converte o espaço livre de bytes para Megabytes (MB)
        disco_bytes = psutil.disk_usage('/').free
        self.valor = round(disco_bytes / (1024 * 1024), 2)
        return self.valor

def registrar_metricas(metricas: list, nome_arquivo: str = "metricas.csv"):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepara as linhas para salvar no CSV
    linhas = []
    for m in metricas:
        m.coletar()  # Polimorfismo: chama o coletar específico de cada subclasse
        linhas.append([agora, m.nome, m.valor, m.unidade])

    # Escreve ou adiciona os registros no CSV
    arquivo_existe = False
    try:
        with open(nome_arquivo, "r"):
            arquivo_existe = True
    except FileNotFoundError:
        arquivo_existe = False

    with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if not arquivo_existe:
            # Se o arquivo for novo, insere o cabeçalho
            escritor.writerow(["datetime", "metrica", "valor", "unidade"])
        
        escritor.writerows(linhas)
    
    print(f"[{agora}] ✅ Métricas gravadas no arquivo '{nome_arquivo}'.")

def main():
    print("=== COLETOR DE MÉTRICAS DO SISTEMA (DEVOPS) ===")
    
    # Desafio B: escolha do arquivo e métricas
    nome_arquivo = input("Nome do arquivo CSV [padrão: metricas.csv]: ").strip()
    if not nome_arquivo:
        nome_arquivo = "metricas.csv"
        
    if not nome_arquivo.endswith(".csv"):
        nome_arquivo += ".csv"

    print("\nQuais métricas deseja coletar?")
    print("1 - Todas (CPU, Memória e Disco)")
    print("2 - Apenas CPU")
    print("3 - Apenas Memória")
    print("4 - Apenas Disco")
    
    opcao = input("Escolha uma opção (1-4): ").strip()
    
    metricas = []
    if opcao == "2":
        metricas = [CpuMetrica()]
    elif opcao == "3":
        metricas = [MemoriaMetrica()]
    elif opcao == "4":
        metricas = [DiscoMetrica()]
    else:
        metricas = [CpuMetrica(), MemoriaMetrica(), DiscoMetrica()]

    # Desafio A: coleta periódica (loop)
    try:
        intervalo = int(input("\nIntervalo entre coletas (em segundos) [padrão: 5]: ") or 5)
        iteracoes = int(input("Quantidade de iterações [padrão: 10]: ") or 10)
    except ValueError:
        intervalo = 5
        iteracoes = 10

    print(f"\n🚀 Iniciando monitoramento: {iteracoes} coletas a cada {intervalo}s...\n")

    for i in range(1, iteracoes + 1):
        print(f"--- Coleta {i}/{iteracoes} ---")
        registrar_metricas(metricas, nome_arquivo)
        
        if i < iteracoes:
            time.sleep(intervalo)

    print("\n🎉 Monitoramento concluído com sucesso!")


if __name__ == "__main__":
    main()

