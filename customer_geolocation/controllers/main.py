# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ansil pv (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#####################################################################################
"""
 Install geopy package to decoding geocodes and vise versa
"""
import json
import pytz
from geopy import Nominatim
from odoo import http
from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalGeolocation(CustomerPortal):
    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, **post):
        """ Super CustomerPortal class function and pass the api key value from settings using params to website view
        file"""

        res = super(PortalGeolocation, self).account(**post)
        params = request.env['ir.config_parameter'].sudo()
        values = params.get_param(
            'base_geolocalize.google_map_api_key')
        res.qcontext.update({
            'api': values
        })
        return res


class GeoChanger(http.Controller):
    @http.route(['/geo/change/<coordinates>'], type='json', auth="none", website=False, csrf=False)
    def geo_changer(self, coordinates):
        """Controller function for get address details  from latitude and longitude that we pinpointed in map using geopy
            package from python

        Parameters
        ----------
        coordinates :The stringify value from map that contains latitude and longitude

        Returns
        -------
        Returning the address details back to view file from the converted Latitude and longitude
        """
        data = {}
        res = json.loads(coordinates)
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(res.get('lat')) + "," + str(res.get('lng')))
        if location:
            addresses = location.raw['address']
            if addresses.get('village'):
                city = addresses.get('village')
            else:
                city = "Undefined"
            if addresses.get('suburb'):
                suburb = addresses.get('suburb')
            else:
                suburb = "Undefined"
            state = addresses.get('state')
            country_code = addresses.get('country_code')
            country = pytz.country_names[country_code]
            if addresses.get('postcode'):
                p_code = addresses.get('postcode')
            else:
                p_code = "Undefined"
        else:
            city = "Undefined"
            suburb = "Undefined"
            state = "Undefined"
            country_code = "Undefined"
            country = "Undefined"
            p_code = "Undefined"
        data.update({
            'city': city,
            'suburb': suburb,
            'state': state,
            'country': country,
            'p_code': p_code,
        })
        return data


class GeoLocation(http.Controller):
    @http.route(['/geo/location/<address>'], type='json', auth="none", website=False, csrf=False)
    def geo_location(self, address):
        """ Get value from city field in 'my_account' page and convert into lat and long and return back to website and
            set the map and fields
        Parameters
        ----------
        address : The city name that in city field in website

        Returns
        -------
        Pass the value to website view and set required fields and map

        """
        data = {}
        print(address, "address")
        locator = Nominatim(user_agent="myGeocoder")
        print("locator", locator)
        location = locator.geocode(address)
        print("location", location)
        geolocator = Nominatim(user_agent="geoapiExercises")
        location_country = geolocator.reverse(str(location.latitude) + "," + str(location.longitude))
        addresses = location_country.raw['address']
        country_code = addresses.get('country_code')
        country = pytz.country_names[country_code]
        if location.latitude:
            latitude = location.latitude
            print("latitrude", location.latitude)
        else:print("qwert")
        if location.longitude:
            longitude = location.longitude
            print("longitude", location.longitude)
        else:print("qwerty")
        if addresses.get('postcode'):
            p_code = addresses.get('postcode')
        else:
            p_code = "undefined"
        data.update({
            'lat': latitude,
            'lng': longitude,
            'country': country,
            'p_code': p_code
        })
        return data
