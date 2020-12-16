Test Suite and automation
=========================

A series of unit and integration tests are run automatically with every pull
request or merge to the Github repository. Running the tests locally is also
possible by running pytest from the paramak based directory.

.. code-block:: bash

   pip install pytest

.. code-block:: bash

   pytest tests

The status of the tests is available on the CircleCI account
`CircleCI account. <https://app.circleci.com/pipelines/github/ukaea/paramak?branch=main>`_ 

The test suite can be explored on the
`Gihub source code repository. <https://github.com/ukaea/paramak/tree/main/tests>`_ 

In addition to automated tests we also have automated code style formatting
using  `autopep8 and Github Actions. <https://github.com/ukaea/paramak/actions?query=workflow%3Aautopep8>`_ 

Continuing the theme of automation we also have automated distribution updates.
The distribution is performed by `PyPI <https://pypi.org/>`_ and this is kept
upto date using Github Actions
`(upload python package) <https://github.com/ukaea/paramak/actions?query=workflow%3A%22Upload+Python+Package%22>`_ 
which trigger on every merge to the main branch.

There are also plans for a continiously updated Dockerhub image in the pipeline.
