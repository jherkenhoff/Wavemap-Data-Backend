from setuptools import setup

setup(name="data_backend",
      version="0.1",
      description="Daten-Backend fuer das PJET2018 Projekt",
      url="https://dl0ht.fk4.hs-bremen.de/git/jherkenhoff/Data-Backend",
      author="jherkenhoff",
      author_email="jherkenhoff@stud.hs-bremen.de",
      license="MIT",
      packages=["data_backend"],
      install_requires=[
        "h5py",
        "numpy"
      ],
      zip_safe=False)
