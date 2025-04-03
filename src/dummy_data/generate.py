#!/usr/bin/env -S uvx --with numpy --with polars python
# -*- coding: utf-8 -*-

import os
import argparse
from pathlib import Path
import logging
from numpy import random
from polars import DataFrame

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Generate dummy data")
    argparser.add_argument(
        "--output", type=str, required=True, help="Output directory"
    )
    args = argparser.parse_args()
    output_dir = args.output
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)


    seeds = [0, 1, 2, 3, 4]
    n_columns = 10
    n_rows = 1000

    for seed in seeds:
        random.seed(seed)
        df = DataFrame({
            f"column_{i}": random.rand(n_rows) for i in range(n_columns)
        })

        output_file = Path(output_dir, f"data_{seed}.csv")
        logger.debug(f"Writing to {output_file}")
        df.write_csv(output_file)
