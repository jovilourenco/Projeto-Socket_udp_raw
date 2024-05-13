import socket
import random

END_SERVIDOR = ('server_ipv4', 50000)

# Função que envia requisição e aguarda resposta do servidor.
def envia_requisicao(requisicao_tipo, identificador):

    # ========== Abre o socket e envia requisição ==========

    # Formato da mensagem a ser enviada: req/tipo (1byte) + identificador(2bytes)
    requisicao_msg = int.to_bytes(requisicao_tipo, 1, 'big') + \
                  int.to_bytes(identificador, 2, 'big')

    sock.sendto(requisicao_msg, END_SERVIDOR)

    # ========== Aguarda resposta do servidor ==========
    resposta_msg, servidor_end = sock.recvfrom(2048)
    payload_tamanho = int.from_bytes(resposta_msg[3:4], 'big')

    if(requisicao_tipo == 2): #Tratar resposta quando o for um inteiro.
        payload = int.from_bytes(resposta_msg[4:4 + payload_tamanho], 'big')
    else: #Tratar resposta quando for string.
        payload = resposta_msg[4:4 + payload_tamanho].decode()

    print(f'Resposta: {payload}')

def main():

    while True:
        print("\nEscolha o tipo de requisição:")
        print("1. Data e hora atual;")
        print("2. Mensagem motivacional para o fim do semestre;")
        print("3. Quantidade de respostas emitidas pelo servidor até agora;")
        print("4. Sair.")
        requisicao_tipo = int(input())

        identificador = random.randint(1, 65535)

        if requisicao_tipo == 1:
            envia_requisicao(0, identificador)
        elif requisicao_tipo == 2:
            envia_requisicao(1, identificador)
        elif requisicao_tipo == 3:
            envia_requisicao(2, identificador)
        elif requisicao_tipo == 4:
            print("Saindo...")
            break
        else:
            sock.close()
            print("\nOpção inválida, escolha novamente.")
            continue

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    main()