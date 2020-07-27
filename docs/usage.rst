=====
Usage
=====

To use pnadc in a project::

	import pnadc
	
.. _header-n524:

Extract
=======

.. _header-n525:

pnadc.get( quarter, year, ... , \**kwargs )
-------------------------------------------

.. _header-n526:

Description:
~~~~~~~~~~~~

Download the desired survey database and return a pandas DataFrame.

.. _header-n528:

*parms*:
~~~~~~~~

[mandatory]

-  quarter: int or str - desired survey quarter

-  input_file: int or str -desired survey year

[options]

-  path: str - full ending repository to download and extract data
   (defaults to where the script is being executed) WARNING: PATH's MUST
   END WITH A CLOSING BAR

-  get_docs: Boolean - choose to download (True, default) or not
   (False) doc files in select_files. If you don't have a input file
   in the given directory you should keep it at default.

-  select_files: list - select which doc files you wish to
   download/extract. Defaults to only the input file. Empty list []
   means all doc files will be extract and replaced. To see which doc
   files are available you can use the Advanced Extract method
   \**pnadc.extract.query*\ docs()**.

-  keep_columns: list - build the DataFrame only with the desired column
   list

-  del_file: Boolean - choose to delete (True, default) or keep (False)
   the origin .txt pnadc file.

-  sy: Boolean - saves file without loading it if True. Default is
   False.

-  \**kwargs

.. _header-n552:

pnadc.get_all( range_years, ... , \**kwargs )
-------------------------------------------------

.. _header-n553:

Description:
~~~~~~~~~~~~

Download the desired survey database year range and save them as csv.

.. _header-n555:

*parms*:
~~~~~~~~

[mandatory]

-  range_years: list or range - years to iterate and download all
   PNADc's data

[options]

-  path: str - full ending repository to download and extract data
   (defaults to where the script is being executed) WARNING: PATH's MUST
   END WITH A CLOSING BAR

-  get_docs: Boolean - choose to download (True, default) or not
   (False) doc files in select_files. If you don't have a input file
   in the given directory you should keep it at default.

-  select_files: list - select which doc files you wish to
   download/extract. Defaults to only the input file. Empty list []
   means all doc files will be extract and replaced. To see which doc
   files are available you can use the Advanced Extract method
   \**pnadc.extract.query_docs()**.

-  keep_columns: list - build the DataFrame only with the desired column
   list

-  del_file: Boolean - choose to delete (True, default) or keep (False)
   the origin .txt pnadc file.

-  sy: Boolean - saves file without loading it if True. Default is
   False.

-  \**kwargs

.. _header-n577:

pnadc.get_all( quarter, year, ... , \**kwargs )
-----------------------------------------------

.. _header-n578:

Description:
~~~~~~~~~~~~

Download the desired survey database and return a pandas DataFrame.

.. _header-n580:

*parms*:
~~~~~~~~

[mandatory]

-  quarter: int or str - desired survey quarter

-  input_file: int or str -desired survey year

[options]

-  path: str - full ending repository to download and extract data
   (defaults to where the script is being executed) WARNING: PATH's MUST
   END WITH A CLOSING BAR

-  get_docs: Boolean - choose to download (True, default) or not
   (False) doc files in select*\ files. If you don't have a input file
   in the given directory you should keep it at default.

-  select_files: list - select which doc files you wish to
   download/extract. Defaults to only the input file. Empty list []
   means all doc files will be extract and replaced. To see which doc
   files are available you can use the Advanced Extract method
   \**pnadc.extract.query*\ docs()**.

-  keep_columns: list - build the DataFrame only with the desired column
   list

-  del_file: Boolean - choose to delete (True, default) or keep (False)
   the origin .txt pnadc file.

-  sy: Boolean - False

-  \**kwargs

.. _header-n603:

Build, Save, Unzip and Query
============================

.. _header-n604:

pnadc.build( data_file, input_file='input_PNADC_trimestral.txt' )
-------------------------------------------------------------------------

.. _header-n605:

Description:
~~~~~~~~~~~~

Return the given PNADC_0XXXXX.txt file into a pandas dataframe.

.. _header-n607:

*parms*:
~~~~~~~~

[mandatory]

-  data_file: str- the pnadc .txt file to be loaded

-  input_file: str -the .txt dictionary file. Defaults to
   'input_PNADC_trimestral.txt', expecting it in the same directory

[options]

-  keep_columns: list - build the DataFrame only with the desired column
   list

-  del_file: Boolean - choose to delete (True, default) or keep (False)
   the origin .txt pnadc file.

.. _header-n620:

pnadc.save( df, name )
----------------------

.. _header-n621:

Description:
~~~~~~~~~~~~

| Enhancements needed.
| Only saves the current DataFrame with it's .to_csv method

.. _header-n623:

*parms*:
~~~~~~~~

[mandatory]

-  df : pd.DataFrame - the pandas DataFrame object to be saved.

-  name: str- name or path+name of the file to be saved without the
   extension.

.. _header-n630:

pnadc.unzip( file_name, ... )
-----------------------------

.. _header-n631:

Description:
~~~~~~~~~~~~

Unpack the given zipped file in its given directory.

.. _header-n633:

*parms*:
~~~~~~~~

[mandatory]

-  df : pd.DataFrame - the pandas DataFrame object to be saved.

[options]

-  keep_zipfile: Boolean - delete the origin zipfile if False. Default
   is True.

.. _header-n643:

pnadc.query(q, input_file='input_PNADC_trimestral.txt' )
------------------------------------------------------------

.. _header-n644:

Description:
~~~~~~~~~~~~

Returns a python dictionary containing the survey description about a
desired variable.

.. _header-n646:

Example:
~~~~~~~~

.. code:: python

   # Supossing input file in the same directory
   In [1]: import pnadc as pdc
   In [2]: pdc.query("V1028")
   Out[2]: {'column': 'V1028', 'desc': 'Peso COM pós estratificação'}

.. _header-n649:

*parms*:
~~~~~~~~

[mandatory]

-  q : str - query variable

-  input_file: str - the .txt dicionary file. Defaults to
   'input_PNADC_trimestral.txt' , expecting it in the same directory

.. _header-n656:

Tools
=====

.. _header-n657:

pnadc.tools.identify( df, ... )
-------------------------------

.. _header-n658:

Description:
~~~~~~~~~~~~

Identify houses (longitudinal) and/or individuals (not longitudinal) by
creating respectively df['keyDom'] and/or df['keyInd'] keys and
returnning them with the DataFrame.

.. _header-n660:

*parms*:
~~~~~~~~

[mandatory]

-  df : pd.DataFrame - the PNADC pandas dataframe to be loaded

[options]

-  key: str or NoneType - the desired key levels to be created

   -  args: 'dom' (houses), 'ind' (individuals) or None ( both, default)

-  UPA, V1008, V1014, V2003: variables used to create the keys. They
   default to same name strings.

.. _header-n675:

pnadc.tools.deflators( df, defl_file )
--------------------------------------

.. _header-n676:

Description:
~~~~~~~~~~~~

| Merge and return the current pandas DataFrame with their respectively
  deflators from the doc files, creating a mergeble key
  df['uf_tri_ano'] to match the df['def_Habitual'] (usual
  deflator) and df['def_Efetivo'] (effective deflator).
| Assumes that you df contains UF, Ano and Trimestre columns.

.. _header-n678:

*parms*:
~~~~~~~~

[mandatory]

-  df : pd.DataFrame - the PNADC pandas DataFrame to be loaded

-  defl_file: str - the excel file with the deflators provided in the
   official docs

.. _header-n685:

Advanced Extract
================
[building]


