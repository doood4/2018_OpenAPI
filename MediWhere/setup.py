from distutils.core import setup, Extension

setup(
    name = "MediWhere",
    version = "1.0",
    classifiers=["MediWhere"],
    data_files=[("MediWhere",
	["MediWhere\kpu_logo.gif",
	 "MediWhere\MediWhere_icon.ico",
	 "MediWhere\MediWhere_logo.gif"]
	 	)],
    packages=["MediWhere"]
)