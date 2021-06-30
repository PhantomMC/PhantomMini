/*
 LCLO Phantom Server (C Edition)

 This Source Code Form is subject to the terms of the Mozilla Public
 License, v. 2.0. If a copy of the MPL was not distributed with this
 file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
*/

#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>

#define PROTOCOL 0
#define PORT 25104

void assert(bool valid, char msg[])
{
	if (valid)
		return;
	perror(msg);
	exit(EXIT_FAILURE);
}

int main(int argc, char const *argv[])
{
	int server_fd, new_socket, valread;
	struct sockaddr_in address;
	int opt = 1;
	int addrlen = sizeof(address);
	char buffer[1024] = {0};
	char *hello = "Hello from server";

	// Creating socket file descriptor
	assert(!((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0), "socket failed");

	// Forcefully attaching socket to the port PORT
	assert(!(setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
						&opt, sizeof(opt))),
		   "setsockopt");

	address.sin_family = AF_INET;
	address.sin_addr.s_addr = INADDR_ANY;
	address.sin_port = htons(PORT);

	// Forcefully attaching socket to the port PORT
	assert(!(bind(server_fd, (struct sockaddr *)&address,
				  sizeof(address)) < 0),
		   "bind failed");

	assert(!(listen(server_fd, 3) < 0), "listen");

	assert(!((new_socket = accept(server_fd, (struct sockaddr *)&address,
								  (socklen_t *)&addrlen)) < 0),
		   "accept");

	valread = read(new_socket, buffer, 1024);
	printf("%s\n", buffer);
	send(new_socket, hello, strlen(hello), 0);
	printf("Hello message sent\n");
	return 0;
}
