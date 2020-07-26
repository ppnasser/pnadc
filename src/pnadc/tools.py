# -*- coding: utf-8 -*-

from .pypnad import *

__all__ = ['identify', 'deflators']


def identify(df, key=None, UPA="UPA", V1008='V1008', V1014='V1014', V2003='V2003'):
    if key is None:
        df['keyDom'] = df[UPA].apply(str) + df[V1008].apply(str) + df[V1014].apply(str)
        df['keyInd'] = df[UPA].apply(str) + df[V1008].apply(str) + df[V1014].apply(str) + df[V2003].apply(str)
        return df
    elif 'dom' == key:
        df['keyDom'] = df[UPA].apply(str) + df[V1008].apply(str) + df[V1014].apply(str)
    elif 'ind' == key:
        df['keyInd'] = df[UPA].apply(str) + df[V1008].apply(str) + df[V1014].apply(str) + df[V2003].apply(str)
    else:
        raise ValueError("Avaliable parameters are: dom, ind and None")
    return df


def deflators(df, defl_file):
    """"""
    f = pd.read_excel(defl_file)
    f = f.loc[(f.trim == '01-02-03') |
              (f.trim == '04-05-06') |
              (f.trim == '07-08-09') |
              (f.trim == '10-11-12'),
              :].rename(columns={'trim': 'Trimestre',
                                 'Habitual': 'def_Habitual',
                                 'Efetivo': 'def_Efetivo'})

    def tri(x):
        if x == '01-02-03':
            return 1
        elif x == '04-05-06':
            return 2
        elif x == '07-08-09':
            return 3
        else:
            return 4

    f['Trimestre'] = f["Trimestre"].apply(tri)
    f['uf_tri_ano'] = f["UF"].apply(str) + f["Trimestre"].apply(str) + f["Ano"].apply(str)
    f = f[['uf_tri_ano', 'def_Habitual', 'def_Efetivo']]

    df['uf_tri_ano'] = df["UF"].apply(str) + df["Trimestre"].apply(str) + df["Ano"].apply(str)

    return pd.merge(df, f, how='left', on='uf_tri_ano')
