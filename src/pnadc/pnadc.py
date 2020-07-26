# -*- coding: utf-8 -*-

from .pypnad import *
from .tools import *

__all__ = ['unzip', 'extract', 'build', 'query', 'get', 'get_all']

_URL_PNAD = 'ftp://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/'
_URL_DOCS = 'ftp://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/Documentacao/'


def unzip(file_name, keep_zipfile=True):
    print("Unziping", file_name)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()
    print("Unzip complete")
    if not keep_zipfile:
        os.remove(file_name)
    return file_name[:-3]+"txt"


class extract:

    def _downloader(search, query_url, path,unzip_file, **kwargs):
        print("Downloading", search, "this can take some time.")
        urllib.request.urlretrieve(query_url, path + search)
        print(search, "download is complete!")
        if unzip_file and search[-3:] == "zip":
            return unzip(path+search, **kwargs)

    def data(quarter, year, path='', unzip_file=True, **kwargs):

        try:
            quarter = int(quarter)
            url = _URL_PNAD + str(year)
            text = str(urllib.request.urlopen(url).read().decode('utf-8'))
            search = re.findall('PNADC_0+'+str(quarter)+str(year)+'.*\.zip', text)
            if not search:
                print("Query 0"+str(quarter)+str(year)+" not found.")
                raise Exception
            else:
                query_url = url + '/' + search[0]
                return extract._downloader(search=search[0], query_url=query_url,
                                           path=path, unzip_file=unzip_file, **kwargs)
        except Exception as e:
            print(e)
            return

    def query_docs():
        text = str(urllib.request.urlopen(_URL_DOCS).read().decode('utf-8'))
        pattern = '([A-z_0-9-]+\.xls|[A-z_0-9-]+\.zip|[A-z_0-9-]+\.pdf|[A-z_0-9-]+\.xlsx)'
        return re.findall(pattern=pattern, string=text)

    def docs(path='', select_files=[], unzip_file=True, **kwargs):

        try:
            search = extract.query_docs()
            if not search:
                print("Nothing found.")
                raise Exception
            else:
                if not select_files:
                    select_files = search
                extract._extract_docs(search=search, path=path,
                                      select_files=select_files,
                                      unzip_file=unzip_file,
                                      **kwargs)
        except Exception as e:
            print(e)
            pass

    def _extract_docs(search, path, select_files, unzip_file, **kwargs):
        for i in search:
            if i in select_files:
                query_url = _URL_DOCS + i
                extract._downloader(search=i, query_url=query_url, path=path,
                                    unzip_file=unzip_file, **kwargs)


def build(data_file, input_file='input_PNADC_trimestral.txt', keep_columns=[], del_file=True):
    return pyPNAD.load(data_file, input_file, del_file=True, keep_columns=keep_columns)


def query(q, input_file='input_PNADC_trimestral.txt'):
    columns, widths, var = pyPNAD.col_widths(input_file)
    var = [{'column': i['name'], 'desc': i['comment']} for i in var]
    return next((item for item in var if item["column"] == q), None)


def get(quarter, year, path='', get_docs=True, keep_columns=[], select_files=['Dicionario_e_input.zip'], sy=False, **kwargs):
    if get_docs:
        extract.docs(path=path, select_files=select_files, **kwargs)
    data_file = extract.data(quarter=quarter, year=year, path=path, **kwargs)
    data = build(data_file, path+'input_PNADC_trimestral.txt', keep_columns=keep_columns)
    if not sy:
        return data
    if sy:
        save(data, path+'PNADC_0'+str(quarter)+str(year))


def get_all(range_years, path='', get_docs=True, keep_columns=[], select_files=['Dicionario_e_input.zip'], **kwargs):
    if get_docs:
        extract.docs(path=path, select_files=select_files, **kwargs)

    for year in range_years:
        for quarter in [1, 2, 3, 4]:
            data_file = extract.data(quarter=quarter, year=year, path=path, **kwargs)

            if data_file is None:
                break
            else:
                data = build(data_file, path+'input_PNADC_trimestral.txt', keep_columns=keep_columns)
                save(data, path+'PNADC_0'+str(quarter)+str(year))
                del data


def save(df, name):
    """first release note: enhancements needed for new output formats"""
    print("Saving .csv")
    df.to_csv(name+'.csv')
    print(name+'.csv', 'saved!')
