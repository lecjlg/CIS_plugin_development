#! /usr/bin/python2.7
# vim: tabstop=4 expandtab
import logging
from cis.data_io.products.AProduct import AProduct
from cis.data_io.netcdf import read_many_files_individually, get_metadata

class aws(AProduct):

    def get_file_signature(self):
        return [r'aws*\.nc']

    def create_coords(self, filenames, usr_variable=None):
        from cis.data_io.Coord import Coord, CoordList
        from cis.data_io.ungridded_data import UngriddedCoordinates
        from cis.exceptions import InvalidVariableError

        variables = [("longitude", "x"), ("latitude", "y"), ("altitude", "z"), ("time", "t"), ("relative_humidity", "RH")]

		logging.info("Listing coordinates: " + str(variables))

        coords = CoordList()
        for variable in variables:
             try:
                 var_data = read_many_files_individually(filenames,variable[0])[variable[0]]
                 coords.append(Coord(var_data, get_metadata(var_data[0]),axis=variable[1]))
             except InvalidVariableError:
                 pass
        return UngriddedCoordinates(coords)


    def create_data_object(self, filenames, variable):
        from cis.data_io.ungridded_data import UngriddedData
        usr_var_data = read_many_files_individually(filenames,variable)[variable]

        coords = self.create_coords(filename)

        return UngriddedData(usr_var_data, get_metadata(usr_var_data[0]),coords)
