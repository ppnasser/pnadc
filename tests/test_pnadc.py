
from pnadc.cli import main
import pnadc
import pandas as pd
import pytest
import re
import os

PATH = os.path.dirname(os.path.abspath(__file__))+'/'

@pytest.fixture(scope="module")
def df():
    df = pd.read_csv(PATH+"PNADC_TEST.csv")
    df = df.to_string(float_format="%.0f")
    return df

def test_main():
    assert main([]) == 0


def test_build(df):
    DF = pnadc.build(PATH+"PNADC_TEST.txt", 
                     input_file=PATH+'input_PNADC_trimestral.txt',
                     del_file=False)
    DF = DF.to_string(float_format="%.0f")
    assert DF == df


def test_api_ftp():
    text = pnadc.extract._url_response(pnadc.extract._URL_PNADC)
    search = re.findall('Documentacao', text)
    if not search:
        assert False
    else:
        assert True

if __name__=='__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
