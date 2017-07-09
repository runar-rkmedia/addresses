"""Retrieval-functions for getting address-data from database"""
if __name__ == '__main__':
    from model_pymongo import collection
else:
    from .model_pymongo import collection



def get_post_area_for_post_code(post_code):
    """Return the post-area for a postcode."""
    address = collection.find_one({
        'post_code': post_code
    })
    if address:
        return address["post_area"]
    else:
        raise ValueError(
            'Did not find an address matching {}'.format(post_code))


def get_post_code_for_post_area(post_area):
    """Return the post-code for a post-area."""
    addresses = collection.find(
        {
            'post_area':
                {
                    '$regex': "^" + post_area,
                    '$options': 'i'
                }
        },
        {
            'post_code': 1
        }
    ).distinct('post_code')
    if addresses:
        return addresses
    else:
        raise ValueError(
            'Did not find an address matching {}'.format(post_area))


def get_address_from_street_name(
        street_name,
        contains=True,
        near_post_code=0,
        limit=10
):
    """
    Return the post-code for a street_name.

    street_name: the street to lookup e.g. Kings Road
    contains: default to True, to do partial matches. False for strict matches
    near_post_code: provide a post_code, and will order by closest to.
    limit: default to 10. Max entries to retrieve. use None to get all.
    """
    if contains:
        addresses = collection.aggregate([
            {'$match': {'street_name': {'$regex': "^" + street_name,
                                        '$options': 'i'}}},
            {'$project': {'diff': {'$abs': {'$subtract': [
                near_post_code, '$post_code']}}, 'doc': '$$ROOT'}},
            {'$sort': {'diff': 1}},
            {'$limit': limit},
        ])
        formated_adresses = []
        for address in addresses:
            formated_adresses.append(address['doc'])
        addresses = formated_adresses
    else:
        addresses = collection.find(
            {
                'street_name': street_name
            },
            {
                '_id':0
            }
        )
    if addresses:
        return addresses
    else:
        raise ValueError(
            'Did not find an address matching {}'.format(street_name))


if __name__ == '__main__':
    pass
