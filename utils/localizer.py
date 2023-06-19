def localize_region(slug: str):
    regions = [
        {'slug': 'nyc1', 'name': 'New York 1'}, {'slug': 'nyc2', 'name': 'New York 2'}, {'slug': 'nyc3', 'name': 'New York 3'},
        {'slug': 'sfo1', 'name': 'San Fransisco 1'}, {'slug': 'sfo2', 'name': 'San Fransisco 2'}, {'slug': 'sfo3', 'name': 'San Fransisco 3'},
        {'slug': 'ams2', 'name': 'Amsterdam 2'}, {'slug': 'ams3', 'name': 'Amsterdam 3'},
        {'slug': 'sgp1', 'name': 'Singapura 1'}, {'slug': 'lon1', 'name': 'London 1'},
        {'slug': 'fra1', 'name': 'Perancis 1'}, {'slug': 'blr1', 'name': 'Bandolore 1'},
        {'slug': 'tor1', 'name': 'Toronto 1'},
    ]

    for region in regions:
        if region['slug'] == slug:
            return region['name']

    return slug
