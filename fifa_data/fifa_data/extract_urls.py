import click
from rejson import Client, Path


@click.command()
@click.option("--key_from", help="Redis key to extract urls from.")
@click.option("--key_to", help="Redis key to extract urls to.")
@click.option("--url_path", help="ReJSON path where url is stored in.")
def extract_urls(key_from, key_to, url_path):

    for key in rj.scan_iter(f'{key_from}:item:*'):
        url = rj.jsonget(key, Path(f'.{url_path}'))
        rj.sadd(f'{key_to}:start_urls', url)

    print('url_count' + '=' + str(rj.scard(f'{key_to}:start_urls')))


if __name__ == '__main__':

    rj = Client(host='localhost', port=6379, decode_responses=True)
    extract_urls()
