#!/usr/bin/env python3
"""
Test psycopg with CockroachDB.
"""
import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg2
from psycopg2.errors import SerializationFailure

def upsert_ref(conn, k):
    with conn.cursor() as cur:
        cur.execute("insert into ref (select key, random() from fact, generate_series(1, 1000) where key =%s);" %k )
        logging.info("inserted fact key  %s ", k)
        logging.debug("insert: status message: %s", cur.statusmessage)
        conn.commit()

def main():
    opt = parse_cmdline()
    print(opt)
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)

    conn = psycopg2.connect(opt.dsn)

    # print_balances(conn)
    for i in range(0, 1000000):
        n = 0
        while true:
            n += 1
            if (n == 10):
                throw Error("did not succeed within 10 retries")
            try:
                upsert_ref(conn, i)

            # The function below is used to test the transaction retry logic.  It
            # can be deleted from production code.
            # run_transaction(conn, test_retry_loop)
            except ValueError as ve:
            # Below, we print the error and continue on so this example is easy to
            # run (and run, and run...).  In real code you should handle this error
            # and any others thrown by the database interaction.
                if ve.code != "40001":
                    throw error
                else:
                    conn.exec('ROLLBACK;')
                    sleep(int(((2**n) * 100) + rand( 100 - 1 ) + 1))
                logging.debug("run_transaction(conn, ) failed: %s", i)

    # Close communication with the database.
    conn.close()


def parse_cmdline():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "dsn",
        help="database connection string\n\n"
             "For cockroach demo, use postgresql://<username>:<password>@<hostname>:<port>/bank?sslmode=require,\n"
             "with the username and password created in the demo cluster, and the hostname and port listed in the\n"
             "(sql/tcp) connection parameters of the demo cluster welcome message.\n\n"
             "For CockroachCloud Free, use 'postgres://<username>:<password>@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/<cluster-name>.bank?sslmode=verify-full&sslrootcert=<your_certs_directory>/cc-ca.crt',\n"
             "If you are using the connection string copied from the Console, your username, password, and cluster name will be pre-populated.\n"
             "Replace <your_certs_directory> with the path to the cc-ca.cert downloaded from the Console."
    )

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print debug info")

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    main()
