import socket
import random

CLIENTE_PORTA = 59155
SERVIDOR_PORTA = 50000
END_SERVIDOR = ('server_ipv4', 50000)

# Função que envia requisição e aguarda resposta do servidor.
def envia_requisicao(tipo_de_requisicao, requisicao):

    #Criando o cabeçalho udp: porta de origem + porta destino + comprimento (0x000B) + checksum
    cabecalho_do_udp = CLIENTE_PORTA.to_bytes(2) + SERVIDOR_PORTA.to_bytes(2) + b"\x00\x0b" + calcula_checksum(requisicao)


    sock.sendto(cabecalho_do_udp + requisicao, END_SERVIDOR)

    # ========== Aguarda resposta do servidor ==========
    resposta_msg, servidor = sock.recvfrom(1024)

    # Verifica se o remetente é o ip do professor. Se não for, continua esperando.
    while servidor[0] != 'server_ipv4':
        resposta_msg, servidor = sock.recvfrom(1024)

    # Se o tipo de requisição for 3, convertemos o payload para um valor inteiro.
    if tipo_de_requisicao == 3:
        resposta_sem_cabecalhos = int.from_bytes(resposta_msg[32:], 'big')
    else:
        resposta_sem_cabecalhos = resposta_msg[32:].decode()

    print(f"\nResposta: {resposta_sem_cabecalhos}")

# Função que calcula o checksum.
def calcula_checksum(payload_requisicao):
    ip_local = socket.gethostbyname(socket.gethostname()).split(".")

    # Formato do meu ip: b'\xc0'.b'\xa8'.b'\x00'.b'\x08' (192.168.0.8)
    # Para formar as porções de 2 bytes como na especificação, temos que fazer: b'\xc0' * 256 = b'\xc0\x00'
    # Assim, pode-se fazer a soma com o primeiro e o segundo índice: b'\xc0\x00' + b'\xa8' = b'\xc0\xa8' e assim por diante...
    soma_cabecalho_ip = (int(ip_local[0]) * 256 + int(ip_local[1]) + int(ip_local[2]) * 256 + int(ip_local[3]) + 0x0FE4 + 0xBF6D + 0x0011 + 0x000B)

    # Soma porções do cabeçalho do segmento udp com padding
    soma_cabecalho_udp = 0xE713 + 0xC350 + 0x000B + 0x0000

    # Soma das porções de 2 bytes do pseudo cabeçalho IP, do cabeçalho UDP e do payload da requisição
    somatorio = soma_cabecalho_ip + soma_cabecalho_udp + int.from_bytes(payload_requisicao[:2]) + int.from_bytes(payload_requisicao[2:] + b"\x00")
    
    # Pega os bits mais significativos, desloca para a direita.
    separa_bits_a_direita = somatorio >> 16
    separa_bits_a_esquerda = somatorio & 0xFFFF

    #Faz o wraparound e aplica o complemento de 1.
    checksum = (~(separa_bits_a_direita + separa_bits_a_esquerda)) & 0xFFFF
    checksum = checksum.to_bytes(2)
    return checksum

def main():

    while True:
        print("\nEscolha o tipo de requisição:")
        print("1. Data e hora atual;")
        print("2. Mensagem motivacional para o fim do semestre;")
        print("3. Quantidade de respostas emitidas pelo servidor até agora;")
        print("4. Sair.")
        requisicao_tipo = int(input(""))

        identificador = random.randint(1, 65535).to_bytes(2)

        if requisicao_tipo == 1:
            envia_requisicao(requisicao_tipo, b"\x00" + identificador)
        elif requisicao_tipo == 2:
            envia_requisicao(requisicao_tipo, b"\x01" + identificador)
        elif requisicao_tipo == 3:
            envia_requisicao(requisicao_tipo, b"\x02" + identificador)
        elif requisicao_tipo == 4:
            print("Saindo...")
            sock.close()
            break

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    main()
