import os
from imap_tools import MailBox, AND

# pegar emails de um remetente para um destinatário
username = "diplan.proplan@ufopa.edu.br"
password = "dp2019"

titulo = "Execução 2024 - sem RapsInscritos"
pasta_destino = "C:\\Users\\usuario\\Nextcloud\\Documents\\Relatórios\\Documentos_Paineis_Orcamentarios"

# lista de imaps: https://www.systoolsgroup.com/imap/
meu_email = MailBox('mail.ufopa.edu.br').login(username, password)

# criterios: https://github.com/ikvk/imap_tools#search-criteria
lista_emails = meu_email.fetch(AND(from_="lista-cdsdw@serpro.gov.br", subject="Execucao 2024 - sem RapsInscritos")) 

# pegar emails com um anexo específico
lista_emails = meu_email.fetch(AND(from_="lista-cdsdw@serpro.gov.br"))
for email in lista_emails:
    if len(email.attachments) > 0:
        anexo_salvo = False  # Variável de controle para verificar se o anexo foi salvo
        for anexo in email.attachments:
            if titulo in anexo.filename:
                caminho_arquivo = os.path.join(pasta_destino, "Execucao 2024 - sem RapsInscritos.csv")
                with open(caminho_arquivo, 'wb') as arquivo_excel:
                    arquivo_excel.write(anexo.payload)
                    print("Anexo salvo com sucesso.")
                    anexo_salvo = True  # Atualiza a variável de controle
                    break  # Sai do loop interno
        if anexo_salvo:
            break  # Sai do loop externo se o anexo for salvo com sucesso
    else:
        print("Nenhum anexo encontrado.")
