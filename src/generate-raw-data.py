#!/usr/bin/env -S uvx --with numpy --with polars python
# -*- coding: utf-8 -*-

from numpy import random
from polars import DataFrame

if __name__ == "__main__":
    seeds = [0, 1, 2, 3, 4]
    n_columns = 10
    n_rows = 1000

    for seed in seeds:
        random.seed(seed)
        df = DataFrame({
            f"column_{i}": random.rand(n_rows) for i in range(n_columns)
        })
        df.write_csv(f"data/raw/data_{seed}.csv")
