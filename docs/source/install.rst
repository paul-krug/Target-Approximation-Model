Installation instructions
^^^^^^^^^^^^^^^^^^^^^^^^^

pypi
~~~~
The simplest way to install *Target-Approximation-Model* is through the Python Package Index (PyPI).
This will ensure that all required dependencies are fulfilled.
This can be achieved by executing the following command::

    pip install Target-Approximation-Model

or::

    sudo pip install Target-Approximation-Model

to install system-wide, or::

    pip install -u Target-Approximation-Model

to install just for your own user.



Source
~~~~~~

If you've downloaded the archive manually from the `releases
<https://github.com/paul-krug/TargetApproximationModel/releases/>`_ page, you can install using the
`setuptools` script::

    tar xzf TargetApproximationModel-VERSION.tar.gz
    cd TargetApproximationModel-VERSION/
    python setup.py install

If you intend to develop librosa or make changes to the source code, you can
install with `pip install -e` to link to your actively developed source tree::

    tar xzf TargetApproximationModel-VERSION.tar.gz
    cd TargetApproximationModel-VERSION/
    pip install -e .

Alternately, the latest development version can be installed via pip::

    pip install git+https://github.com/paul-krug/TargetApproximationModel
