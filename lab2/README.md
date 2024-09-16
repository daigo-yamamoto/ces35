# Servidor e Cliente de Arquivos com Protocolo Personalizado

Este projeto implementa um servidor e um cliente de arquivos utilizando sockets em C, com um protocolo de aplicação personalizado. O servidor atende requisições de múltiplos clientes simultaneamente, permitindo a obtenção de arquivos e a consulta do último acesso realizado pelo cliente.

## Descrição

O projeto consiste na implementação de um servidor de arquivos e um cliente que se comunicam através de sockets TCP utilizando um protocolo de aplicação personalizado. O protocolo define dois comandos principais:

1. MyGet `<arquivo>`: O cliente solicita ao servidor o envio de um arquivo específico.

2. MyLastAccess: O cliente solicita ao servidor o instante do último acesso realizado por ele mesmo.

O servidor mantém o estado de cada cliente individualmente, armazenando o timestamp do último acesso. A aplicação foi desenvolvida para ser robusta, à prova de problemas de rede e de usuário, e utiliza threads para atender múltiplos clientes simultaneamente.

## Funcionalidades

- **Serivdor**:
    - Atende múltiplos clientes simultaneamente utilizando threads.
    - Processa comandos personalizados do cliente.
    - Envia arquivos solicitados pelos clientes.
    - Mantém o registro do ultimo cesso de cada cliente

- **Cliente**:
    - Conecta-se ao servidor e envia comandos personalizados.
    - Recebe e exibe o conteúdo dos arquivos solicitados
    - Pode solicitar informações sobre o último acesso.

## Instalação e Compilação

### Clonar o repositório

    git clone <url da pagina>

Dentro do repositorio, compile os arquivos em C.

    gcc server.c -o server -lpthread
    gcc client.c -o client -lpthread

## Execução

### Iniciando o servidor

Execute o seguinte comamdno no terminal para iniciar o servidor:

    ./server

O servidor estará rodando na porta 8080 por padrão.

### Iniciando o cliente

Em outro terminal, execute o cliente:

    ./client

O cliente tenstará se conectar ao servidor local na porta 8080.

## Como utilizar

Após a inicialiadao do cliente e do servidor, voce poderá digitar os seguintes comandos:

- **MyGet** `<arquivo>`: Solicita ao servidor o arquivo especificado.
- **MyLastAccess**: Solicita ao servidor o instante do último acesso realizado por este cliente.

### Exemplo de uso

1. Solicitando um arquivo

    MyGet exemplo.txt

- O servidor enviará o conteúdo do arquivo `exemplo.txt`
- Certifique-se que o arquivo esteja e exista no diretorio onde o servidor está sendo executado.

2. Verificando o último acesso:

    MyLastAccess

- Se for a primeira vez acessando, o servidor responderá `Last Acess=Null`
- Após alguma requisição `MyGet`, o servidor retornará o timestamp do último acesso.