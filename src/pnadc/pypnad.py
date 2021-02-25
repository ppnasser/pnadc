# -*- coding: utf-8 -*-

"""
pyPNAD v3.0
July 2020 release

The purpose of this code is to import PNADC microdata,
released by the Brazilian Office of Statistics (IBGE), into a
pandas DataFrame in a simple and straightforward fashion.

This code was originally written by Lincoln de Sousa.
The original code can be found on https://github.com/clarete/pnad
It was then simplified and updated by Carlos Góes in October 2017
https://github.com/omercadopopular/cgoes/tree/master/TinyApps/pyPNAD .

This last version was modifyed by Patrick Nasser, July 2020, in order to support dataframe
building from pynadc package.

The load() and col_widths() module were modifyed from previous version and
_build() fuction was added. Docststrings were also modifyed to improve clarity.

------------------------------------------------------------------------------
pyPNAD v2.0
October 2017 release

The purpose of this code is to import PNAD and PNADC microdata,
released by the Brazilian Office of Statistics (IBGE), into a
pandas DataFrame in a simple and straightforward fashion.

This code was originally written by Lincoln de Sousa.
The original code can be found on https://github.com/clarete/pnad
It was then simplified and updated by Carlos Góes in October 2017.

The procedure is quite simple. The load() function requires two
parameters. You can call it by using the following steps:

pyPNAD.load(data_file, input_file)

* data_file is a the raw text file that holds the microdata for
    every PNAD and PNAD.
* input_file is a SAS variable dictionary, which is a companion file to
    the microdata and contains variable names, text positions, and lenghts.

"""

import io
import multiprocessing as mp
import os
from math import ceil
from multiprocessing.pool import ThreadPool

import pandas as pd
from tqdm import tqdm


class pyPNAD:
    def get_var(line):
        "Parse through dictionary line, return column names and widths"
        # Read
        position, rest = line.split(' ', 1)
        variable, rest = rest.strip().split(' ', 1)
        size, rest = rest.strip().split(' ', 1)
        comment = rest.replace('/*', '').replace('*/', '').strip()

        # Convert
        position = int(position.replace('@', ''))
        variable = variable.strip()
        size = int(float(size.replace('$', '')))

        return {
            'name': variable,
            'position': position,
            'size': size,
            'comment': comment,
        }

    def get_vars(varsfile):
        """return a colection of names, positions, sizes, and labels"""
        variables = []
        for line in varsfile:
            if line[0] == '@':
                variable = pyPNAD.get_var(line)
                variables.append(variable)
            else:
                pass
        return variables

    def col_widths(vars_file):
        """Parse through all variables in PNAD"""

        vars_fp = io.open(vars_file, encoding='latin-1')
        variables = pyPNAD.get_vars(vars_fp)

        columns = [var['name'] for var in variables]
        widths = [var['size'] for var in variables]

        return columns, widths, variables

    def load(data_file, input_file, **kwargs):
        """Loads all input and source files, returns a pandas DataFrame"""
        print('Building', data_file)
        columns, widths, var = pyPNAD.col_widths(input_file)
        return pyPNAD._build(data_file, widths=widths, names=columns, **kwargs)

    def _build(data_file, widths, names,
               keep_columns=[], del_file=True):

        ctx = mp.get_context('spawn')
        pool = ThreadPool(ctx.Semaphore(mp.cpu_count()).get_value())

        def df_chunking(chunk, keep_columns=keep_columns):
            """Splits df into chunks, drops data of original df inplace"""
            pbar.update(1)
            if keep_columns and isinstance(keep_columns, list):
                return chunk[keep_columns]
            else:
                return chunk

        chunksize = 2e4
        chunks = pd.read_fwf(data_file, widths=widths,
                             header=None, names=names,
                             chunksize=chunksize)

        print('Multiprocessing chunks')
        pbar = tqdm(total=ceil(sum(1 for row in open(data_file, 'r')) / chunksize))

        to_concat = pool.imap_unordered(df_chunking, chunks)

        data = pd.concat(list(to_concat))
        data[data.columns] = data[data.columns].apply(pd.to_numeric,
                                                      errors='coerce', axis=1)
        pool.close()
        pool.join()
        if del_file:
            os.remove(data_file)
        pbar.close()
        print('Done!')
        return data

    def __init__(self):
        self.release = 'Feb 2021'
        self.version = '3.1'
        self.author = 'Lincoln de Souza & Carlos Góes & Patrick Nasser'
