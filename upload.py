import pypi
 
packpath = "pycountries.py"
pypi.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="PyCountries",
                   description=".",
                   url="http://github.com/karimbahgat/PyCountries",
                   keywords="data world countries geography GIS",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 4 - Beta",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop',
                                "Topic :: Scientific/Engineering :: GIS"],
                   )

pypi.generate_docs(packpath)
#pypi.upload_test(packpath)
#pypi.upload(packpath)

