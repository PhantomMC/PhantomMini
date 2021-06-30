/*
 LCLO Phantom Server (C Edition)

 This Source Code Form is subject to the terms of the Mozilla Public
 License, v. 2.0. If a copy of the MPL was not distributed with this
 file, You can obtain one at http://mozilla.org/MPL/2.0/.

 @author: Thorin
*/

#include <stdio.h>


int listen(){

	while(1){
		char input[];
		gets( input );
		switch (input){
		case "stop":
			printf("stop command")
			return 0;
		case "restart":
			printf("restart command")
			return 1;
		default:
			printf("Unknown command")
		}

	}
}
