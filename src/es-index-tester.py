"""
Script used to make a KNN search to an ES index
"""
import argparse
import logging
import sys
import random
import math

try:
    from elasticsearch import Elasticsearch
except ImportError:
    logging.error("Python libraries not installed")
    exit(1)


def run(
    es_host: str,
    es_index: str,
    es_user: str,
    es_psw: str,
    vector_dim: int,
    es_index_embedding_field: str = "embedding",
    normalize_vector: bool = True,
    knn_results: int = 100,
    knn_candidates: int = 1000,
):
    es_client = Elasticsearch(
        hosts=es_host,
        basic_auth=(es_user, es_psw),
        opaque_id="es-index-tester@client",
        request_timeout=5,
        max_retries=3,
    )
    if not es_client.ping():
        logging.error("ES not connected.")
        exit(1)

    vector = [random.random() for _ in range(vector_dim)]
    if normalize_vector:
        logging.info("Normalizing the vector...")
        vector = [num / math.sqrt(sum(num**2 for num in vector)) for num in vector]

    es_query = {
        "field": es_index_embedding_field,
        "query_vector": vector,
        "k": knn_results,
        "num_candidates": knn_candidates,
    }

    logging.info(f"Quering {knn_results} KNN results from {es_index}...")
    results = es_client.search(index=es_index, knn=es_query, size=knn_results)
    logging.info(f"Query completed! Results:{str(results)[:1000]}...")
    exit(0)


def cmdline_args():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    p.add_argument("--es_host", type=str, required=True, help="")
    p.add_argument("--es_index", type=str, required=True, help="")
    p.add_argument("--es_user", type=str, required=True, help="")
    p.add_argument("--es_psw", type=str, required=True, help="")
    p.add_argument("--vector_dim", type=int, required=True, help="")
    p.add_argument(
        "-d",
        "--debug",
        help="Enable debug logging statements",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )

    p.add_argument(
        "-q",
        "--quiet",
        help="Disable info logging statements",
        action="store_const",
        dest="loglevel",
        const=logging.WARNING,
        default=logging.INFO,
    )
    return p.parse_args()


if __name__ == "__main__":
    if sys.version_info < (3, 7, 0):
        sys.stderr.write("You need python 3.7 or later to run this script\n")
        sys.exit(1)

    try:
        args = cmdline_args()
    except Exception as e:
        logging.error(f"Error during command parsing: `{e}`")
        sys.exit(1)

    logging.basicConfig(level=args.loglevel)
    run(
        es_host=args.es_host,
        es_index=args.es_index,
        es_user=args.es_user,
        es_psw=args.es_psw,
        vector_dim=args.vector_dim,
    )
