MAX_CUBES_STORED = 4

ZONE_0_STORE_LOCATION_0 = {'x': 0.5, 'y': 7.5}
ZONE_0_STORE_LOCATION_1 = {'x': 1, 'y': 7.5}
ZONE_0_STORE_LOCATION_2 = {'x': 0.5, 'y': 7}
ZONE_0_STORE_LOCATION_3 = {'x': 1, 'y': 7}
ZONE_0_STORE_LOCATIONS = [ZONE_0_STORE_LOCATION_0, ZONE_0_STORE_LOCATION_1, ZONE_0_STORE_LOCATION_2, ZONE_0_STORE_LOCATION_3]
ZONE_0_RETURN_LOCATION_012 = {'x': 1, 'y': 7}
ZONE_0_RETURN_LOCATION_3 = {'x': 1.5, 'y': 6.5}
ZONE_0_RETURN_LOCATIONS = [ZONE_0_RETURN_LOCATION_012, ZONE_0_RETURN_LOCATION_012, ZONE_0_RETURN_LOCATION_012, ZONE_0_RETURN_LOCATION_3]

ZONE_1_STORE_LOCATION_0 = {'x': 7.5, 'y': 7.5}
ZONE_1_STORE_LOCATION_1 = {'x': 7.5, 'y': 7}
ZONE_1_STORE_LOCATION_2 = {'x': 7, 'y': 7.5}
ZONE_1_STORE_LOCATION_3 = {'x': 7, 'y': 7}
ZONE_1_STORE_LOCATIONS = [ZONE_1_STORE_LOCATION_0, ZONE_1_STORE_LOCATION_1, ZONE_1_STORE_LOCATION_2, ZONE_1_STORE_LOCATION_3]
ZONE_1_RETURN_LOCATION_012 = {'x': 7, 'y': 7}
ZONE_1_RETURN_LOCATION_3 = {'x': 6.5, 'y': 6.5}
ZONE_1_RETURN_LOCATIONS = [ZONE_1_RETURN_LOCATION_012, ZONE_1_RETURN_LOCATION_012, ZONE_1_RETURN_LOCATION_012, ZONE_1_RETURN_LOCATION_3]

ZONE_2_STORE_LOCATION_0 = {'x': 7.5, 'y': 0.5}
ZONE_2_STORE_LOCATION_1 = {'x': 7, 'y': 0.5}
ZONE_2_STORE_LOCATION_2 = {'x': 7.5, 'y': 1}
ZONE_2_STORE_LOCATION_3 = {'x': 7, 'y': 1}
ZONE_2_STORE_LOCATIONS = [ZONE_2_STORE_LOCATION_0, ZONE_2_STORE_LOCATION_1, ZONE_2_STORE_LOCATION_2, ZONE_2_STORE_LOCATION_3]
ZONE_2_RETURN_LOCATION_012 = {'x': 7, 'y': 1}
ZONE_2_RETURN_LOCATION_3 = {'x': 6.5, 'y': 1.5}
ZONE_2_RETURN_LOCATIONS = [ZONE_2_RETURN_LOCATION_012, ZONE_2_RETURN_LOCATION_012, ZONE_2_RETURN_LOCATION_012, ZONE_2_RETURN_LOCATION_3]

ZONE_3_STORE_LOCATION_0 = {'x': 0.5, 'y': 0.5}
ZONE_3_STORE_LOCATION_1 = {'x': 0.5, 'y': 1}
ZONE_3_STORE_LOCATION_2 = {'x': 1, 'y': 0.5}
ZONE_3_STORE_LOCATION_3 = {'x': 1, 'y': 1}
ZONE_3_STORE_LOCATIONS = [ZONE_3_STORE_LOCATION_0, ZONE_3_STORE_LOCATION_1, ZONE_3_STORE_LOCATION_2, ZONE_3_STORE_LOCATION_3]
ZONE_3_RETURN_LOCATION_012 = {'x': 1, 'y': 1}
ZONE_3_RETURN_LOCATION_3 = {'x': 1.5, 'y': 1.5}
ZONE_3_RETURN_LOCATIONS = [ZONE_3_RETURN_LOCATION_012, ZONE_3_RETURN_LOCATION_012, ZONE_3_RETURN_LOCATION_012, ZONE_3_RETURN_LOCATION_3]

STORE_LOCATIONS = [ZONE_0_STORE_LOCATIONS, ZONE_1_STORE_LOCATIONS, ZONE_2_STORE_LOCATIONS, ZONE_3_STORE_LOCATIONS]
RETURN_LOCATIONS = [ZONE_0_RETURN_LOCATIONS, ZONE_1_RETURN_LOCATIONS, ZONE_2_RETURN_LOCATIONS, ZONE_3_RETURN_LOCATIONS]

class ReturnManager():
    
    def __innit__(self, zone):
        self.store_locations = STORE_LOCATIONS[zone]
        self.return_locations = RETURN_LOCATIONS[zone]
        self.cubes_stored = 0
        
    def getReturnLocation(self):
        
        if (self.cubes_stored == MAX_CUBES_STORED):
            return None
        
        else:
            return_location = self.return_locations[self.cubes_stored]
            return return_location
        
    def getStoreLocations(self):
        
        if (self.cubes_stored == MAX_CUBES_STORED):
            return None
        
        else:
            store_location = self.store_locations[self.cubes_stored]
            self.cubes_stored += 1
            return store_location
        