import click
from pymongo import MongoClient
from rejson import Client, Path

from fifa_data.mongodb_addr import host, port


def pull_from_redis(keys,
                    client=Client(decode_responses=True),
                    path=Path.rootPath()):

    insert_queue = list()

    for key in client.scan_iter(keys):
        insert_queue.append(client.jsonget(key, path))

    return insert_queue


def push_to_mongodb(db,
                    collection,
                    insert_queue,
                    client=MongoClient(host, port)):

    db = client[db]
    collection = db[collection]

    # TODO find a way to upsert results to avoid duplicate values
    # TODO look at inserting in batches
    result = collection.insert_many(insert_queue)

    # TODO find a substitute to bulk_api_result to print out resutls
    return result


def flush_redis(keys, client=Client()):

    for key in client.scan_iter(keys):
        client.delete(key)


@click.command()
@click.option("--keys", help="RedisJSON key pattern to extract values from.")
@click.option("--db", help="MongoDB database to store documents in.")
@click.option("--collection", help="MongoDB collection to store documents in.")
def main(keys, db, collection):

    try:
        push_to_mongodb(db=db,
                        collection=collection,
                        insert_queue=pull_from_redis(keys=keys))

    except Exception:
        print('Error in updating db')

    finally:
        flush_redis(keys=keys)


if __name__ == '__main__':

    main()
