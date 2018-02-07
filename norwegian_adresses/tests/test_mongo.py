# -*- coding: utf-8 -*-
"""Unit-tests for adresses."""
# import os
import unittest

from norwegian_adresses import NorAddress

nor_address = NorAddress()

known_values_postareas = {
    'Kristiansand S': [
        4632, 4612, 4628, 4629, 4630, 4634, 4622, 4631, 4618, 4617, 4626, 4613,
        4635, 4621, 4636, 4615, 4624, 4610, 4638, 4620, 4614, 4616, 4637, 4639, 4623,
        4611, 4633, 4608,
    ]}

known_values_post_codes = {
    4633: 'Kristiansand S',
    8250: 'Rognan'
}

known_values_street_name = {
    'Kongens gate':
        {
            'post_codes': [1606, 1530, 1809, 153, 3510, 3611, 3210, 3211, 3717, 4610, 4608, 6002, 7011, 7013, 7012, 7715, 7713, 8006, 8514, 9950, 9900],
            'post_areas': ['FREDRIKSTAD', 'MOSS', 'ASKIM', 'OSLO', 'HØNEFOSS', 'KONGSBERG', 'SANDEFJORD', 'SANDEFJORD', 'SKIEN', 'KRISTIANSAND S', 'KRISTIANSAND S', 'ÅLESUND', 'TRONDHEIM', 'TRONDHEIM', 'TRONDHEIM', 'STEINKJER', 'STEINKJER', 'BODØ', 'NARVIK', 'VARDØ', 'KIRKENES']
        },
    'Bergtoras vei': {'post_codes': [4633], 'post_areas': ['KRISTIANSAND S']},
    'Justnesveien': {'post_codes': [4634], 'post_areas': ['KRISTIANSAND S']},
}


class AddressKnownValuesTests(unittest.TestCase):
    """Test lookup of adresses in db."""

    def test_by_post_code(self):
        """Test getting post_area for a post-code"""
        for key, value in known_values_post_codes.items():
            area = nor_address.by_post_code(key)['post_area']
            self.assertEqual(area.lower(), value.lower())

    def test_post_codes_by_post_area(self):
        """Test getting post_code for a postal area."""
        for key, value in known_values_postareas.items():
            result = nor_address.post_codes_by_post_area(key)
            self.assertCountEqual(result, value)

    def test_by_street_name(self):
        """Test getting addresses by street_name."""
        result = nor_address.by_street_name('Bergtoras vei 2', 4633)
        from pprint import pprint
        self.assertEqual(result['loc'], [58.16957350413589, 8.028893827316551])

    def test_by_street_name_closest_to(self):
        """Test against known values for street_names"""
        for key, value in known_values_street_name.items():
            results = nor_address.by_street_name_closest_to(key, limit=1000)
            r_post_code = [r['post_code'] for r in results]
            self.assertCountEqual(r_post_code, value['post_codes'])


if __name__ == '__main__':
    unittest.main()
