# Automação de Email com AWS Lambda e AWS ECR

## PROBLEMA

Salvar um anexo de email do serviço de email institucional da UFOPA e fazer upload para a Nuvem da UFOPA.

## FLUXO DE TRABALHO

1. Conectar ao serviço de email institucional da UFOPA.
2. Baixar o anexo do email do remetente especificado.
3. Conectar ao serviço de Nuvem da UFOPA.
4. Fazer upload do arquivo para a pasta de destino.

## SISTEMA OPERACIONAL

Ubuntu 22.04

## PACOTES UTILIZADOS

- nextcloud-client
- python3
- python3-pip
- python3-venv
- software-properties-common

## BIBLIOTECAS PYTHON UTILIZADAS

- imap_tools
- awslambdaric

## PROGRAMAS UTILIZADOS

- Docker Desktop
- AWS CLI

## INSTALANDO OS PROGRAMAS

1. Baixe e instale o Docker Desktop para Windows: [Docker Desktop Installer](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64)

2. Siga o [tutorial de instalação do Docker](https://docs.docker.com/desktop/install/windows-install/#install-docker-desktop-on-windows).

3. Baixe e instale o AWS CLI: [AWS CLI Installer](https://awscli.amazonaws.com/AWSCLIV2.msi)

   Mais informações sobre o AWS CLI podem ser encontradas [aqui](https://aws.amazon.com/pt/cli/).

## 1. CRIANDO A IMAGEM DO CONTAINER PARA USAR NO AWS ECR

O arquivo `Dockerfile` contém todas as informações para a criação da imagem personalizada, como variáveis de ambiente, bibliotecas e permissões necessárias para o funcionamento correto do programa.

O arquivo `script_email.py` contém os comandos para a automação da tarefa junto com o fluxo de execução e logs necessários para o acompanhamento da execução do código. É este código que será executado para que a automação aconteça.

## 2. CONSTRUINDO A IMAGEM DO SO

No terminal, dentro da pasta onde estão os arquivos, execute o comando abaixo para construir (build) a imagem personalizada do SO Ubuntu 22.04 com o código de automação e as bibliotecas necessárias. O termo 'lambda-ubuntu22v1' será o nome da imagem personalizada.

```bash
docker build -t lambda-ubuntu22v1 .
```

## 3. CRIANDO UM REPOSITÓRIO PRIVADO NO AWS ECR

É necessário criar um repositório privado no AWS ECR, que servirá como local onde você salvará a sua imagem do SO personalizado na AWS.

Para isso, acesse o AWS ECR, defina a região onde o repositório será criado e clique no botão "Criar repositório". Escolha se o repositório será público ou privado (padrão), defina o nome do repositório e clique em "Criar repositório".

## 4. CONECTANDO COM O AWS ECR

Agora que a imagem do SO e o repositório foram criados, precisamos conectar o AWS CLI com o AWS ECR para enviar a imagem para o repositório da AWS ECR.

Para isso, precisamos de uma chave de acesso da AWS que permita a conexão entre o AWS CLI e os serviços da AWS. No menu do usuário, clique em "Credenciais de segurança", desça até a opção "Chave de acesso" e clique em "Criar chave de acesso".

Aceite o aviso de segurança caso seja um usuário root da AWS e clique em "Criar chave de acesso". Com isso, serão criadas a chave de acesso e a chave de acesso secreta. Você precisa das duas para conectar o AWS CLI com os serviços da AWS.

**NÃO SAIA DA PÁGINA DE CHAVE DE ACESSO ATÉ TERMINAR DE CONFIGURAR O AWS CLI. VOCÊ SÓ PODE VER A CHAVE DE ACESSO SECRETA APENAS UMA VEZ.**

### 4.1 CONFIGURANDO O AWS CLI NO TERMINAL

No terminal, digite o seguinte comando:

```bash
aws configure
```

O terminal irá solicitar as seguintes informações:

- **AWS Access Key ID [****************]:** copie e cole a chave de acesso que você criou na etapa anterior.
- **AWS Secret Access Key [****************]:** copie e cole a chave de acesso secreta que você criou na etapa anterior.
- **Default region name [us-east-1]:** digite `us-east-1` (ou a região preferida).
- **Default output format [None]:** pressione Enter.

Pronto, as configurações do AWS CLI estão prontas. Caso seja necessário, repita esta etapa.

### 4.2 FAZENDO LOGIN NO AWS ECR

Execute o seguinte comando para fazer login no AWS ECR:

```bash
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com
```

Altere os termos `REGION` pela região do seu repositório no AWS ECR que você escolheu, e `AWS_ACCOUNT_ID` pelo ID da sua conta AWS.

Se tudo der certo, uma mensagem de "Login Succeeded" será exibida.

## 5. SUBINDO A IMAGEM DO SO PARA O AWS ECR

Agora que terminamos de configurar e conectar o AWS ECR ao AWS CLI, podemos enviar a nossa imagem personalizada para o nosso repositório no AWS ECR.

Para isso, digite os seguintes comandos no terminal:

```bash
docker tag IMAGEM AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/REPOSITORY

docker push AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/REPOSITORY
```

Altere os termos:
- `IMAGEM` pelo nome da imagem personalizada que você criou.
- `AWS_ACCOUNT_ID` pelo ID da sua conta AWS.
- `REGION` pela região do seu repositório AWS ECR.
- `REPOSITORY` pelo nome do seu repositório criado no AWS ECR.

Se tudo der certo, você verá uma saída parecida com esta no terminal:

```
The push refers to a repository [aws_account_id.dkr.ecr.region.amazonaws.com/hello-repository] (len: 1)
e9ae3c220b23: Pushed
a6785352b25c: Pushed
0998bf8fb9e9: Pushed
0a85502c06c9: Pushed
latest: digest: sha256:215d7e4121b30157d8839e81c4e0912606fca105775bb0636EXAMPLE size: 6774
```

Você pode ver mais dicas na documentação do [AWS ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html)

## 6. CRIANDO E CONFIGURANDO A FUNÇÃO LAMBDA A PARTIR DA IMAGEM DO AWS ECR

1. Entre no AWS Lambda na mesma região do seu repositório do AWS ECR.
2. Clique em "Criar função".
3. Na página seguinte, escolha a opção "Imagem de contêiner" para podermos usar a nossa imagem personalizada.
4. Dê um nome para a função Lambda.
5. Clique em "Procurar imagem" para escolher a imagem a ser usada na função Lambda e selecione o seu repositório.
6. Marque a imagem que deseja usar e clique em "Selecionar imagem".
7. Clique em "Criar função".

### 6.1 DEFININDO O EVENTO (TRIGGER) QUE IRÁ INICIAR A FUNÇÃO LAMBDA

Para que a função possa ser iniciada, devemos definir qual evento (trigger) iniciará nossa função Lambda. Podemos escolher vários eventos, de acordo com o objetivo da nossa função, mas nesse caso, a função Lambda será iniciada de segunda a sexta-feira, às 8:00 da manhã.

1. Clique no botão "+ Adicionar gatilho".
2. Na caixa de seleção da origem do gatilho, selecione a opção "EventBridge (CloudWatch Events)".
3. Vamos definir qual regra do EventBridge vai iniciar a nossa função Lambda, escolha a opção "Criar uma regra".
4. Escolha um nome para a sua regra do EventBridge, a descrição é opcional.
5. No Tipo de regra, marque a opção "Expressão de programação" e no campo de texto da expressão, escreva `cron(0 8 ? * MON-FRI *)`.

   Essa expressão define que o evento gatilho será "Às 8 horas e 0 minutos de segunda a sexta-feira, de qualquer dia, mês ou ano". Altere a expressão de acordo com a necessidade da sua função.

**PARA DEFINIÇÃO DE HORA USANDO O CRON, OS SERVIDORES DA AWS LEVAM EM CONSIDERAÇÃO O HORÁRIO UTC. PODE SER NECESSÁRIO ALTERAR A HORA DO SEU GATILHO USANDO CRON DE ACORDO COM O SEU HORÁRIO LOCAL.**

6. Por último, clique no botão "Adicionar" para concluir a configuração do seu evento gatilho.

### 6.2 TESTANDO A SUA FUNÇÃO LAMBDA

Agora podemos testar a sua função Lambda com a imagem personalizada para ver se tudo ocorrerá como programado.

1. Clique no submenu "Testar" no console AWS Lambda.
2. Crie um evento de teste.
3.

 Defina um nome para o evento de teste, o JSON do evento é opcional.
4. Clique no botão "Testar".

Se tudo estiver configurado corretamente, abrirá uma janela indicando que seu código está em execução. Ao final da execução, serão exibidos os logs de execução da sua função Lambda.

**CASO ALGO DÊ ERRADO, LEIA OS LOGS DE EXECUÇÃO DA FUNÇÃO E FAÇA AS ALTERAÇÕES NECESSÁRIAS.**

## 7. PROJETO FINALIZADO!!

Seu projeto de automação está concluído. Agora ele será executado de forma automática, de acordo com a sua expressão definida no gatilho da função Lambda. Você pode acompanhar os logs usando a ferramenta CloudWatch da AWS.
