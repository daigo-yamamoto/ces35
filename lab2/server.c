#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <time.h>
#include <netinet/in.h>

#define PORT 8080
#define BUFFER_SIZE 1024

typedef struct {
    int socket;
    struct sockaddr_in address;
    time_t last_access;
} client_info;

// Função que lida com cada cliente em uma thread separada
void *handle_client(void *arg) {
    client_info *client = (client_info *)arg;
    char buffer[BUFFER_SIZE];
    int valread;

    // Loop para comunicação contínua com o cliente
    while ((valread = read(client->socket, buffer, BUFFER_SIZE)) > 0) {
        buffer[valread] = '\0';

        // Processa a mensagem do cliente
        if (strncmp(buffer, "MyGet ", 6) == 0) {
            // Atualiza o último acesso
            client->last_access = time(NULL);

            char *filepath = buffer + 6;
            filepath[strcspn(filepath, "\r\n")] = '\0'; 

            FILE *file = fopen(filepath, "rb");
            if (file == NULL) {
                char *error_msg = "ERROR: File not found\n";
                send(client->socket, error_msg, strlen(error_msg), 0);
            } else {
                char *ok_msg = "OK\n";
                send(client->socket, ok_msg, strlen(ok_msg), 0);

                size_t bytes;
                while ((bytes = fread(buffer, 1, BUFFER_SIZE, file)) > 0) {
                    send(client->socket, buffer, bytes, 0);
                }
                fclose(file);
            }
        } else if (strncmp(buffer, "MyLastAccess", 12) == 0) {
            // Verifica se houve acesso anterior
            if (client->last_access == 0) {
                char *msg = "Last Access=Null\n";
                send(client->socket, msg, strlen(msg), 0);
            } else {
                char msg[BUFFER_SIZE];
                struct tm *timeinfo = localtime(&client->last_access);
                strftime(msg, sizeof(msg), "Last Access=%Y-%m-%d %H:%M:%S\n", timeinfo);
                send(client->socket, msg, strlen(msg), 0);
            }
        } else {
            char *error_msg = "ERROR: Unknown command\n";
            send(client->socket, error_msg, strlen(error_msg), 0);
        }

        memset(buffer, 0, BUFFER_SIZE);
    }

    close(client->socket);
    free(client);
    pthread_exit(NULL);
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Falha ao criar socket");
        exit(EXIT_FAILURE);
    }

    // Configura o endereço e porta
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Liga o socket ao endereço e porta especificados
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Falha no bind");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 10) < 0) {
        perror("Falha no listen");
        exit(EXIT_FAILURE);
    }

    printf("Servidor rodando na porta %d...\n", PORT);

    while ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) >= 0) {
        pthread_t thread_id;
        client_info *client = malloc(sizeof(client_info));
        client->socket = new_socket;
        client->address = address;
        client->last_access = 0;

        // Cria uma nova thread para o cliente
        if (pthread_create(&thread_id, NULL, handle_client, (void *)client) != 0) {
            perror("Falha ao criar thread");
            free(client);
        }
    }

    if (new_socket < 0) {
        perror("Falha no accept");
        exit(EXIT_FAILURE);
    }

    close(server_fd);
    return 0;
}
