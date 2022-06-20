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
#include "lib/protocol/protocol.h"

#define PROTOCOL 0
#define PORT 25104

void assert(int valid, char msg[])
{
	if (valid)
		return;
	perror(msg);
	exit(EXIT_FAILURE);
}

int main(int argc, char const *argv[])
{
	int server_fd;
	int opt = 1;

	// Creating socket file descriptor
	assert(!((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0), "socket failed");

	// Forcefully attaching socket to the port PORT
	assert(!(setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
						&opt, sizeof(opt))),
		   "setsockopt");

	struct sockaddr_in address;
	int addrlen = sizeof(address);
	address.sin_family = AF_INET;
	address.sin_addr.s_addr = INADDR_ANY;
	address.sin_port = htons(PORT);

	// Forcefully attaching socket to the port PORT
	assert(!(bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0), "bind failed");

	assert(!(listen(server_fd, 3) < 0), "listen");

	int new_socket, valread;
	char buffer[1024] = {0};
	char *hello = "Hello from server";
	struct messageInfoData info;
	info.empty = 1;
	while (1)
	{

		assert(!((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0), "accept");

		valread = read(new_socket, buffer, 1024);
		printf("Recieved: %s\n", buffer);
		getMessageInfoData(buffer, (struct messageInfoData *)&info);
		//Write response
		//send response
	}

	return 0;
}
