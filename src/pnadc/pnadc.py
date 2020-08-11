# -*- coding: utf-8 -*-

from .pypnad import *
from .tools import *

__all__ = ['unzip', 'extract', 'build', 'query', 'get', 'get_all']

def unzip(file_name, exdirpath='', keep_zipfile=True):
    """

    Parameters
    ----------
    file_name : TYPE
        DESCRIPTION.
    keep_zipfile : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    print("Unziping", file_name)
    with zipfile.ZipFile(file_name, 'r') as f:
        f.extractall() if exdirpath == '' else f.extractall(exdirpath)
    print("Unzip complete")
    if not keep_zipfile:
        os.remove(file_name)
    return file_name[:-3]+"txt"


class extract:
    _URL_PNADC = 'ftp://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/'
    _URL_DOCS = _URL_PNADC + 'Documentacao/'

    def _url_response(url):
        return str(urllib.request.urlopen(url).read().decode('utf-8'))

    def _downloader(search, query_url, path,unzip_file, **kwargs):
        print("Downloading", search, "this can take some time.")
        urllib.request.urlretrieve(query_url, path + search)
        print(search, "download is complete!")
        if unzip_file and search[-3:] == "zip":
            return unzip(path+search, exdirpath=path, **kwargs)

    def data(quarter, year, path='', unzip_file=True, **kwargs):

        try:
            quarter = int(quarter)
            text = _url_response(extract._URL_PNADC + str(year))
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
        text = _url_response(extract._URL_DOCS)
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
    """Return the given PNADC_0XXXXX.txt file into a pandas dataframe.

    Parameters
    ----------
    data_file : str
        The pnadc .txt file to be loaded.
    input_file : TYPE, optional
        The .txt dictionary file. Defaults The default is 'input_PNADC_trimestral.txt'.
    keep_columns : list, optional
        Build the DataFrame only with the desired column list. The default is [].
    del_file : bool, optional
        Choose to delete (True) or keep (False) the origin .txt pnadc file.
        The default is True.

    Returns
    -------
    data : df.DataFrame
        Returns PNADC DataFrame after building it using pypnad.py file.

    """
    return pyPNAD.load(data_file, input_file, del_file=del_file, keep_columns=keep_columns)


def query(q, input_file='input_PNADC_trimestral.txt'):
    """Returns a python dictionary containing the survey description about
    a desired variable.


    Parameters
    ----------
    q : str
        Query variable.
    input_file : str, optional
        The .txt dicionary file. The default is 'input_PNADC_trimestral.txt'.

    Returns
    -------
    dict
        dict object wtith 'column' and 'desc' as keys.

    """
    columns, widths, var = pyPNAD.col_widths(input_file)
    var = [{'column': i['name'], 'desc': i['comment']} for i in var]
    return next((item for item in var if item["column"] == q), None)


def get(quarter, year, path='', get_docs=True, keep_columns=[], select_files=['Dicionario_e_input.zip'], sy=False, **kwargs):
    """Download the desired survey database year range and save them as csv.

    Parameters
    ----------
    quarter : int or str
        Desired survey quarter.
    year : int or str
        Desired survey year.
    path : str, optional
        Full destiny repository to download and extract data (defaults to where
        the script is being executed). WARNING: PATH’s MUST END WITH A CLOSING BAR.
        The default is ''.
    get_docs : bool, optional
        choose to download (True) or not (False) doc files in select_files.
        If you don’t have a input file in the given directory you should keep
        it at default. The default is True.
    keep_columns : list, optional
        DESCRIPTION. The default is [].
    select_files : list, optional
        Select which doc files you wish to download/extract. The default is
        ['Dicionario_e_input.zip'].
    **kwargs

    Returns
    -------
    data : df.DataFrame
        Returns PNADC DataFrame if sy == False.

    """
    if get_docs:
        extract.docs(path=path, select_files=select_files, **kwargs)
    data_file = extract.data(quarter=quarter, year=year, path=path, **kwargs)
    data = build(data_file, path+'input_PNADC_trimestral.txt', keep_columns=keep_columns)
    if not sy:
        return data
    if sy:
        save(data, path+'PNADC_0'+str(quarter)+str(year))


def get_all(range_years, path='', get_docs=True, keep_columns=[], select_files=['Dicionario_e_input.zip'], **kwargs):
    """Download the desired survey database year range and save them as csv.

    Parameters
    ----------
    range_years : list or range
        Years to iterate and download throgh PNADC data.
    path : str, optional
        Full destiny repository to download and extract data (defaults to where
        the script is being executed). WARNING: PATH’s MUST END WITH A CLOSING BAR.
        The default is ''.
    get_docs : bool, optional
        choose to download (True) or not (False) doc files in select_files.
        If you don’t have a input file in the given directory you should keep
        it at default. The default is True.
    keep_columns : list, optional
        Build the DataFrame only with the desired column list. The default is [].
    select_files : list, optional
        Select which doc files you wish to download/extract. The default is
        ['Dicionario_e_input.zip'].
    **kwargs

    Returns
    -------
    None.

    """
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
    """Enhancements needed.
    Only saves the current DataFrame with it’s .to_csv method

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame object to be saved.
    name : str
        NAME or PATH+NAME of the file to be saved without the extension.

    Returns
    -------
    None.

    """
    print("Saving .csv")
    df.to_csv(name+'.csv',index=False)
    print(name+'.csv', 'saved!')
