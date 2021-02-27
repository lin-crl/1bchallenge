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
        cur.execute("upsert into ref (select key, random() from fact, generate_series(1, 1000) where key =%s);" %k )
        logging.info("upserted fact key  =%s ", k)
        logging.debug("upsert: status message: %s", cur.statusmessage)
        conn.commit()

def main():
    opt = parse_cmdline()
    print(opt)
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)

    conn = psycopg2.connect(opt.dsn)

    # print_balances(conn)
    for i in range(1, 1000001):
        n = 0
        while True:
            n += 1
            if (n == 10):
                raise Exception("did not succeed within 10 retries")
            try:
                upsert_ref(conn, i)
                break
            # The function below is used to test the transaction retry logic.  It
            # can be deleted from production code.
            # run_transaction(conn, test_retry_loop)
            except ValueError as ve:
            # Below, we print the error and continue on so this example is easy to
            # run (and run, and run...).  In real code you should handle this error
            # and any others thrown by the database interaction.
                if ve.code != "40001":
                    raise ve
                else:
                    print(ve, n)
                    conn.execute('ROLLBACK;')
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
             "For cockroach insecure cluster, use postgresql://root@127.0.0.1:26257/defaultdb?sslmode=disable,\n"
    )

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print debug info")

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    main()
