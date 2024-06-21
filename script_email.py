import os
from imap_tools import MailBox, AND

# Configurações
LOCAL_DIR = "/tmp"
REMOTE_DIR = "seuRepositorioRemoto"
SERVER_URL = "www.seuProvedorDeEmail.com"

# Dados de login do email
username = "seuemail@mail.com"
password = "password123"

def handler(event, context):

    # Executa a sincronização
    print("Iniciando sincronização!")
    sync_cmd = f"nextcloudcmd -s --path '{REMOTE_DIR}' '{LOCAL_DIR}' '{SERVER_URL}'"
    sync_result = os.system(sync_cmd)

    if sync_result == 0:
        print("Sincronização concluída com sucesso!")
    else:
        print("Erro na sincronização inicial!")

    # Baixa o email e salva o anexo na pasta /tmp
    print("Baixando arquivo ...")

    # Conectando com o servidor de email
    meu_email = MailBox('mail.provedor.edu.br').login(username, password)
    print("Conectado no servidor de email!")

    # Buscando os emails
    lista_emails = meu_email.fetch(AND(subject="Assunto do email alvo"), charset='UTF-8', reverse=True, limit=1)
    
    for email in lista_emails:
        if len(email.attachments) > 0:
            for anexo in email.attachments:
                informacoes_anexo = anexo.payload
                arquivo_path = os.path.join('/tmp', 'Nome do arquivo salvo')
                with open(arquivo_path, 'wb') as arquivo_excel:
                    arquivo_excel.write(informacoes_anexo)
                    print("Arquivo baixado com sucesso!")
        else:
            print("Erro ao baixar o arquivo!")
            exit(1)

    print("Salvando arquivo na nuvem ...")
    # Sincroniza a pasta com o relatório atualizado
    sync_result = os.system(sync_cmd)

    if sync_result == 0:
        print("Processo Finalizado!")
    else:
        print("Erro na sincronização final!")
        exit(1)
