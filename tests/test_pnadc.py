# -*- coding: utf-8 -*-

import os
import re

import pandas as pd
import pytest

import pnadc
from pnadc.cli import main

PATH = os.path.dirname(os.path.abspath(__file__)) + '/'

@pytest.fixture(scope="module")
def df():
    df = pd.read_csv(PATH + "PNADC_TEST.csv")
    return df

def test_main():
    assert main([]) == 0


def test_build(df):
    data = pnadc.build(PATH + "PNADC_TEST.txt",
                       input_file=PATH + 'input_PNADC_trimestral.txt',
                       del_file=False)
    data = data.to_string(float_format="%.0f")
    DF = df.to_string(float_format="%.0f")
    assert DF == data


def test_api_ftp():
    text = pnadc.extract._url_response(pnadc.extract._URL_PNADC)
    search = re.findall('Documentacao', text)
    assert search != []


def test_mock_get(mocker, df):
    mocker.patch('pnadc.extract.data', return_value=PATH + "PNADC_TEST.txt")
    data = pnadc.get(1, 2020, path=PATH, del_file=False, keep_columns=['Ano'],
                     get_docs=False)
    assert list(df['Ano'].values) == list(data.values)
