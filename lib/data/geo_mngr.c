/*
 LCLO Phantom Server (C Edition)

 This Source Code Form is subject to the terms of the Mozilla Public
 License, v. 2.0. If a copy of the MPL was not distributed with this
 file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
*/

#include <stdio.h>
#include "geo_mngr.h"

// Functions to take an IP input and geolocate it to ISO 3166-1 alpha-2
// Best API for this is probably http://geoip.cdnservice.eu/