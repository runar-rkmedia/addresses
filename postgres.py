"""Create a database of adresses from json-file.."""
import json
import sys
from model import Address, Base, session, engine, AddressQuery
from sqlalchemy import func


def populate_db(data, **kwargs):
    """Poulate a db with adresses."""
    for idx, data_ in enumerate(data):
        for entry in data_:
            # Insert an Address in the address table
            try:
                new_address = Address(
                    street_name=entry.get(kwargs.get('street_name')),
                    post_code=int(entry.get(kwargs.get('post_code'))),
                    post_area=entry.get(kwargs.get('post_area')),
                )
                session.add(new_address)
            except ValueError as e:
                print("\nIgnoring entry: \n{}\nbecause: \n{}\n\nThis is most likely good, as the data doesn't make sense.".format(  # noqa
                    entry, e,
                ))
        print('Added collection {} of {}.'.format(
            idx + 1,
            len(data),
        ))
    print('Saving all entries to database')
    session.commit()
    print('Done')


def json_to_db(json_file, **kwargs):
    """Retrieve all entries in a json-file and add it to db.."""
    with open(json_file) as data_file:
        address_data = json.load(data_file)
    populate_db(address_data[0], **kwargs)


def get_post_area_for_post_code(post_code):
    """Return the post-area for a postcode."""
    address = AddressQuery.filter_by(
        post_code=post_code
    ).first()
    if address:
        return address.post_area
    else:
        raise ValueError(
            'Did not find an address matching {}'.format(post_code))


def get_post_post_code_for_post_area(post_area):
    """Return the post-code for a post-area."""
    addresses = session.query(Address.post_code).filter(
        Address.post_area.ilike(post_area)
    ).group_by(
        Address.post_code
    ).all()
    if addresses:
        post_codes = []
        for address in addresses:
            post_codes.append(address.post_code)
        return post_codes
    else:
        raise ValueError(
            'Did not find an address matching {}'.format(post_area))


def get_address_from_street_name(street_name, contains=True):
    """Return the post-code for a post-area."""
    if contains:
        addresses = AddressQuery\
            .filter(
                func.upper(Address.street_name)
                .contains(func.upper(street_name))
            ).all()
    else:
        addresses = AddressQuery.filter(
            Address.street_name.ilike(street_name)
        ).all()
    if addresses:
        return addresses
    else:
        raise ValueError(
            'Did not find an address matching {}'.format(street_name))


# print(get_post_area_for_post_code(4630))
# print(get_post_area_for_post_code(4631))
# print(get_post_area_for_post_code(4632))
# print(get_post_area_for_post_code(4633))
# print(get_post_post_code_for_post_area('Kristiansand S'))
street_search_results = get_address_from_street_name('åsas')
# street_search_results = get_address_from_street_name('åsas', True)
for result in street_search_results:
    print(result.post_code, result.post_area, result.street_name)


if __name__ == "__main__":
    if "--setup" in sys.argv:
        print('Dropping and reacreating database')
        session.close_all()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        json_to_db(
            'data/adresser.json',
            street_name='vei',
            post_code='postnummer',
            post_area='postnummeromrade'
        )
