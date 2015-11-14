"""# PyCountriesPython module for country information based on online up-to-date data.Country data is retrieved from http://restcountries.eu/, or in the case ofserver downtime uses https://raw.githubusercontent.com/mledoze which is virtuallythe same data. Country geometries are taken from https://github.com/johan/world.geo.json## PlatformsSo far only tested on Python version 2.x. ## DependenciesPure Python, no dependencies. ## Installing itPyCountries is installed with pip from the commandline:    pip install pycountries# UsageThe main use of PyCountries is to be able to easily search for a country,taking into account different name variations and misspellings, or toquickly get a country based on its iso2 or iso3 code....The other very useful feature is the ability to get countries based on a specificcontinent or region:...Or you can create your own country groupings:...Once you have the country, you can query various different attributes suchas......Even more fun is that these country instances provide the __geo_interface__which means you can geographically locate and map the country....Similarly, you can grab the flag of your country as an image (requires PIL):...## More Information:- [Home Page](http://github.com/karimbahgat/PyCountries)- [API Documentation](http://pythonhosted.org/PyCountries)## License:This code is free to share, use, reuse,and modify according to the MIT license, see license.txt## Credits:Karim Bahgat (2015)"""__version__ = "0.1.0"import urllibimport zipfileimport jsonimport ioimport osimport time# Startup# First download country tablestry:    _cachepath = os.path.join(os.path.split(__file__)[0], "_restcountrieseu.txt")    if not os.path.lexists(_cachepath) or (time.time()-os.path.getmtime(_cachepath))/60.0/60.0 > 24:        # download and cache if not exists or older than 24 hrs        APIURL = "http://restcountries.eu/rest/v1"        _raw = urllib.urlopen(APIURL + "/all").read()        with open(_cachepath, "w") as fileobj:            fileobj.write(_raw)    # read from cache    _raw = open(_cachepath).read()    ALLCOUNTRIES = json.loads(_raw)# Or use alternate github download if first failsexcept:        _cachepath = os.path.join(os.path.split(__file__)[0], "_gitcountriesmledoze.txt")    if not os.path.lexists(_cachepath) or (time.time()-os.path.getmtime(_cachepath))/60.0/60.0 > 24:        # download and cache if not exists or older than 24 hrs        APIURL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"        _raw = urllib.urlopen(APIURL).read()        _rawjson = json.loads(_raw)        # make keys same as other source        for country in _rawjson:            country["nativeName"] = country["name"]["native"]            country["officialname"] = country["name"]["official"]            country["name"] = country["name"]["common"]            country["callingCodes"] = country.pop("callingCode")            country["topLevelDomain"] = country["tld"]            country["alpha2Code"] = country.pop("cca2")            country["alpha3Code"] = country.pop("cca3")        with open(_cachepath, "w") as fileobj:            fileobj.write(json.dumps(_rawjson))    # read from cache    _raw = open(_cachepath).read()    ALLCOUNTRIES = json.loads(_raw)# Then download country border coordinatestry:    _cachepath = os.path.join(os.path.split(__file__)[0], "_gitgeojsonjohan.txt")    if not os.path.lexists(_cachepath) or (time.time()-os.path.getmtime(_cachepath))/60.0/60.0 > 24:        # download and cache if not exists or older than 24 hrs        _raw = urllib.urlopen("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json").read()        rawdict = json.loads(_raw)        rawdict = dict( (feat["id"],feat["geometry"]) for feat in rawdict["features"])        with open(_cachepath, "w") as fileobj:            fileobj.write(json.dumps(rawdict))    # read from cache    _raw = open(_cachepath).read()    ALLGEOMS = json.loads(_raw)except:    ALLGEOMS = dict()# Maybe also download and cache flag images?# ...# ...################## Internal Usedef _namesearch_algorithm(name):    "returns a list of matching country dictionaries, only for internal use"    def normalize(text):        text = text.strip().lower()        text = text.replace(","," ").replace(".","").replace("'","")        text = text.replace("-"," ")        text = " ".join(sorted(text.split()))        return text    matches = []    name = normalize(name)    # first check normal match    for countrydict in ALLCOUNTRIES:        official = normalize(countrydict["name"])        alterns = [normalize(alt) for alt in countrydict["altSpellings"][1:]]        if name == official or name in alterns:            matches.append( countrydict )    # if nothing, then the name may have been too long or detailed,    # ...so split name into words, and for each of the    # ...words find if it exactly matches any of the words in the other,    # ...returning only if the match can only be found in one country    if not matches:        for word in name.split():            # maybe for some exceptions this shouldnt be done            # ...eg South + Africa            wordmatches = []            for countrydict in ALLCOUNTRIES:                official = normalize(countrydict["name"])                alterns = [normalize(alt) for alt in countrydict["altSpellings"][1:]]                if word in official.split():                    #print "wordsplit match", word, official                    wordmatches.append( countrydict )                else:                    for altern in alterns:                        if word in altern.split():                            #print "wordsplit match", word, altern                            wordmatches.append( countrydict )                            break                                  # it is a match only if one match could be found            if len(wordmatches) == 1:                matches.append( wordmatches[0] )                break    # if still nothing, then find all countrynames where the name    # ...partially occurs (is a substring of)    if not matches:        for countrydict in ALLCOUNTRIES:            official = normalize(countrydict["name"])            alterns = [normalize(alt) for alt in countrydict["altSpellings"][1:]]            if name in official:                #print "substring match", name, official                matches.append( countrydict )            else:                for altern in alterns:                    if name in altern:                        #print "substring match", name, altern                        matches.append( countrydict )                        break    # if still still nothing, then get difflib most similar    if not matches:        pass    # finished searching    return matches################## User Classesclass Country:    def __init__(self, **kwargs):        """        Represents a country.         Arguments:        - *code* (optional): Either the iso2 or iso3 code of a country.        - *name* (optional): The name of a country. Various nonexact methods are used to find            a match for the country name, including fuzzy matching. Exceptions will be raised if            there are no matches or there are more than one matches. For more flexibility            use instead the find_country() function.         Returns:        - A country instance.        Attributes:        - ...                """                if kwargs.get("code"):            code = kwargs["code"]                     if len(code) == 2: codetype = "alpha2Code"            elif len(code) == 3: codetype = "alpha3Code"            else: raise Exception("The iso code must have a length of 2 or 3")                      for countrydict in ALLCOUNTRIES:                if countrydict[codetype] == code:                    break # code found            else:                raise Exception("Could not find a matching country code, it may be an outdated or a very new code")        elif kwargs.get("name"):            name = kwargs["name"]            matches = _namesearch_algorithm(name)                      if not matches:                raise Exception("Could not find a country by that name")            elif len(matches) == 1:                countrydict = matches[0]            elif len(matches) > 1:                raise Exception("Ambiguous countryname; the name matched with more than one country, please specify the name further or use the 'search_countryname' function for greater flexibility")        else:            raise Exception("To make a country object, specify either a 'code' argument or a 'name' argument")        # rename some of the attributes        self._data = countrydict.copy()        point = self._data.pop("latlng")        self._data["point"] = point        if point:            self._data["point"] = point[1],point[0] # switch to x,y order        self._data["othernames"] = self._data.pop("altSpellings")        self._data["localname"] = self._data.pop("nativeName")        self._data["continent"] = self._data.pop("region")        self._data["region"] = self._data.pop("subregion")        self._data["callcodes"] = self._data.pop("callingCodes")        self._data["webdomains"] = self._data.pop("topLevelDomain")        self._data["iso2"] = self._data.pop("alpha2Code")        self._data["iso3"] = self._data.pop("alpha3Code")    def __getattr__(self, attribute):        if attribute in ("timezones","callcodes","webdomains","currencies","languages"):            return self._data[attribute] or []        else:            return self._data[attribute]    def __str__(self):        return "Country ( %s )" %self.name    def __repr__(self):        return self.__str__()    @property    def __geo_interface__(self):        if hasattr(self, "_cached_geom"):            return self._cached_geom                if self.iso3 in ALLGEOMS and self.iso3 != "SOM": # Johan's Somalia doesnt include Somaliland, so get instead from mledoze below.            return ALLGEOMS[self.iso3]        else:            # the geoms were never loaded on startup or the id could not be found            # ...in the world geofile, so trying the specific country file                        # make geojson string data straight from web. (OLD)            rawtext = urllib.urlopen("https://raw.githubusercontent.com/mledoze/countries/master/data/%s.geo.json" %self.iso3.lower() ).read()            # transform to json            rawdict = json.loads(rawtext)            # get only geometry part            if "geometry" in rawdict["features"][0]:                geodict = rawdict["features"][0]["geometry"]                # cache for later use                self._cached_geom = geodict                ALLGEOMS[self.iso3] = geodict                              return geodict            else:                return Exception("Could not find any available geometry for the country")    @property    def flag(self):        # return gif fileobj straight from web, user decides how to read/process it        if hasattr(self, "_cached_flag"):            return self._cached_flag        urlobj = urllib.urlopen("http://www.geonames.org/flags/x/%s.gif" %self.iso2.lower() )        fileobj = io.BytesIO(urlobj.read())        self._cached_flag = fileobj        return fileobj    @property    def neighbours(self):        return [Country(code=countrycode) for countrycode in self._data["borders"]]    @property    def region(self):        return Region(self._data["region"])       @property    def continent(self):        return Continent(self._data["continent"])class Collection:    def __init__(self, name, countries):        """        Base class for all collections of countries (continents, regions, etc), with all behavior and props defined.        Can also be used for defining your own collection of countries.        Arguments:        - *name*: The desired name of your collection.        - *countries*: A list of country instances belonging to this collection.        Returns:        - A country collection instance.        Attributes:        - ...                """        self.name = name        self.countries = [cntr for cntr in countries] # existing country instances        def __iter__(self):        for country in self.countries:            yield country    def __getattr__(self, attribute):        """        Return a list of all subcountries values for that attribute,        e.g. africa.currency will return a list of all currencies        in Africa.        """        if attribute in ("timezones","callcodes","webdomains","currencies","languages"):            return list(set(listitem for country in self.countries for listitem in country.__getattr__(attribute)))        elif attribute in ("othernames","translations"):            raise Exception("Not very useful to return all possible sets of alternate or translated names, better to just loop and check each")        elif attribute == "gini":            raise Exception("A gini index cannot simply be aggregated from the country level, it requires new calculations on the raw data")        elif attribute in ("localnames","capitals","demonyms"):            return list(set(country.__getattr__(attribute[:-1]) for country in self.countries))        elif attribute == "points":            return list(set(tuple(country.__getattr__("point")) for country in self.countries))        elif attribute in ("population","area"):            return sum(country.__getattr__(attribute) for country in self.countries if country.__getattr__(attribute))        else:            return list(set(country.__getattr__(attribute) for country in self.countries))    def __str__(self):        return "Collection ( %s )" %self.name    def __repr__(self):        return self.__str__()class Continent(Collection):    def __init__(self, name):        """        Represents a continent.        Arguments:        - *name*: Name of a continent.            Valid names:            - Europe            - Oceania            - Africa            - Asia            - Americas        Returns:        - A continent instance.        Attributes:        - ...        """                self.name = name        namelower = name.lower()        self.countries = [Country(code=countrydict["alpha2Code"]) for countrydict in ALLCOUNTRIES                          if countrydict["region"].lower() == namelower]        if not self.countries or not name:            raise Exception("Could not find a continent by that name")    def __str__(self):        return "Continent ( %s )" %self.name    @property    def regions(self):        regionnames = list(set(country.region.name for country in self.countries))        return [Region(name) for name in regionnames] class Region(Collection):    def __init__(self, name):        """        Represents a world region.        Arguments:        - *name*: Name of a world region.            Valid names include:                Caribbean                Middle Africa                Southern Europe                Micronesia                Western Africa                Central Asia                South-Eastern Asia                Eastern Africa                Northern Africa                Eastern Asia                Northern America                Polynesia                Southern Africa                Western Asia                Southern Asia                Melanesia                Australia and New Zealand                Eastern Europe                Northern Europe                Central America                South America                Western Europe        Returns:        - A region instance.        Attributes:        - ...                """        self.name = name        namelower = name.lower()        self.countries = [Country(code=countrydict["alpha2Code"]) for countrydict in ALLCOUNTRIES                          if countrydict["subregion"].lower() == namelower]        if not self.countries:            raise Exception("Could not find a region by that name")    def __str__(self):        return "Region ( %s )" %self.name##class CulturalRegion(Collection):##    # not necessarily exclusive, many different combinations and memberships##    # e.g. Middle East, MENA, Black Sea region, Mediterranean region, etc.##    pass####class IncomeGroup(Collection):##    # e.g. World Bank lower income quintile, etc.##    pass####class MembershipGroup(Collection):##    pass####class DevelopedCountries(Collection):##    pass####class DevelopingCountries(Collection):##    pass################## User functionsdef search_countryname(name):    """    Search for a countryname based on    various nonexact matching criteria including fuzzy matching.    A more flexible alternative than using the Country class directly,    since the Country class will raise an exception if there is not    an exact match.    Arguments:    - **name**: Name of the country you are searching for.    Returns:    - A generator over zero or more county instances matching your search.     """    for countrydict in _namesearch_algorithm(name):        yield Country(code=countrydict["alpha2Code"])def all_countries():    """    Returns a generator of all available country instances.     """    for countrydict in ALLCOUNTRIES:        yield Country(code=countrydict["alpha2Code"])def all_continents():    """    Returns a generator of all available continent instances.     """        continentnames = list(set(countrydict["region"] for countrydict in ALLCOUNTRIES if countrydict["region"]))    for name in continentnames:        yield Continent(name)def all_regions():    """    Returns a generator of all available region instances.     """    regionnames = list(set(countrydict["subregion"] for countrydict in ALLCOUNTRIES if countrydict["subregion"]))    for name in regionnames:        yield Region(name)    