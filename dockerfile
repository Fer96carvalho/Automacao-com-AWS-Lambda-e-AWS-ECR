# Usar Ubuntu 22.04 como base
FROM ubuntu:22.04

# Variáveis de configuração
ENV LOCAL_DIR="/tmp"
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    software-properties-common \
    && apt clean

# Instalar nextcloudcmd
RUN add-apt-repository ppa:nextcloud-devs/client \
    && apt update && apt install -y nextcloud-client

# Criar diretórios de trabalho
RUN mkdir -p $LOCAL_DIR
RUN mkdir -p /home/scripts

# Configurar ambiente virtual
RUN python3 -m venv /home/scripts/venv

# Verificar a instalação do ambiente virtual
RUN ls -l /home/scripts/venv/bin

# Instalar imap_tools no ambiente virtual
RUN /home/scripts/venv/bin/pip install --upgrade pip
RUN /home/scripts/venv/bin/pip install imap_tools
RUN /home/scripts/venv/bin/pip install awslambdaric

# Copiar scripts para o contêiner
COPY script_email.py /home/scripts/script_email.py

# Garantir permissões corretas
RUN chmod +x /home/scripts/script_email.py

# Verificar a existência do script e do interpretador Python
RUN ls -l /home/scripts
RUN ls -l /home/scripts/venv/bin/python3

ENTRYPOINT [ "/home/scripts/venv/bin/python3", "-m", "awslambdaric" ]

# Definir o comando padrão
CMD [ "/home/scripts/venv/bin/python3", "/home/scripts/script_email.py" ]

