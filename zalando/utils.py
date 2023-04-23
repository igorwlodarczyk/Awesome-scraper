import zalando.constants as const


async def get_currency(url):
    for zalando_url in const.currency.keys():
        if zalando_url in url:
            return const.currency[zalando_url]
    return None


def parse_sizes(sizes):
    if not isinstance(sizes, list):
        sizes = [sizes]
    parsed_sizes = []
    for size in sizes:
        if "\n" in size:
            parsed_sizes.append(size.split("\n")[0])
        else:
            parsed_sizes.append(size)
    return parsed_sizes
