#!/usr/bin/env -S uvx --with duckdb --with polars --with pyarrow python
# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path
import duckdb
import polars as pl
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Preprocess data")
    argparser.add_argument(
        "--input", type=str, required=True, help="Input CSV file"
    )
    argparser.add_argument(
        "--output", type=str, required=True, help="Output directory"
    )

    args = argparser.parse_args()

    input_file = Path(args.input)
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file {input_file} does not exist.")

    output_dir = Path(args.output)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    columns_query = f"""
        SELECT column_name
        FROM (
            DESCRIBE SELECT *
            FROM read_csv('{input_file}')
        );
    """
    columns = [col[0] for col in duckdb.sql(columns_query).fetchall()]

    agg_query = 'UNION ALL'.join([f"""
        SELECT
            '{column}' as column,
            MIN({column}) as min,
            MAX({column}) as max,
            AVG({column}) as avg
        FROM read_csv('{input_file}')
    """ for column in columns
    ])

    result = duckdb.sql(agg_query).pl()

    output_file = Path(output_dir, input_file.stem + ".parquet")
    logger.debug(f"Writing to {output_file}")
    result.write_parquet(output_file)
