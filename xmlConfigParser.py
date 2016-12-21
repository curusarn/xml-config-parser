import xml.etree.ElementTree


class XmlConfigParserException(Exception):
    pass


class XmlConfigParser():
    """Parser for XML config files with defined structure

    Attributes:
        cfg (dict of dicts): expected cetegories with expected keys and optionally default values
        root: xmlFile root 
        defaultCategory (string): default category to use when category is omitted during various calls

    """
    def __init__(self, cfgValues, xmlFile, cat=None):
        """Constructor - saves expected keys and default values, loads and validates xmlFile, optionally sets default category

	Args:
	    cfgValues (dict of dicts): expected cetegories with expected keys and optionally default values
	    xmlFile: path to XML config file - file is loaded and validated
            cat (string): default category to use when category is omitted during various calls

	"""
        self.cfg = cfgValues
        self.root = xml.etree.ElementTree.parse(xmlFile).getroot() 
        self.defaultCategory = cat
        
        if self.root is None:
            raise XmlConfigParserException("Xml is malformed - can't find root")


    def parseXmlConfig(self, verbious=False):
        """Main parsing method - extracts keys specified in cfgValues from xmlFile and overwrites default values in cfgValues.
           
	Args:
	    cfgValues (dict of dicts): expected cetegories with expected keys and optionally default values
	    xmlFile (string): path to XML config file - file is loaded and validated
            cat (string): default category to use when category is omitted during various calls

	Returns:
	    Number of read keys from xmlFile

        Raises:
            XmlConfigParserException: on missing key

	"""
        count = 0
        for section, cfg in self.cfg.items():
            if verbious:
                print("CATEGORY: {0} config:".format(section))
            cfgXmlNode = self.root.find(section)

            for key, none in cfg.items():
                if cfgXmlNode is not None:
                    valueNode = cfgXmlNode.find(key)
                    if valueNode is not None:
                        cfg[key] = valueNode.text
                        count += 1
                        if verbious:
                            print("{0}:{1}".format(key, cfg[key]))
                    else:
                        if verbious:
                            print("{0}:{1} (DEFAULT)".format(key, cfg[key]))
                else:
                    if verbious:
                        print("{0}:{1} (DEFAULT)".format(key, cfg[key]))

                if cfg[key] is None:
                    raise XmlConfigParserException("Can't find key '{0}'"
                                                   " in config file"
                                    " (XML structure:/configuration/{1}/{0})"
                                                   .format(key, section))
        
        return count


    def get(self, key, category=None):
        """default getter method to get value for key from config

        Args:
            key (string): key to find in config
            category (string): category to look for key in, when unsfecified use self.defaultCategory

        Returns:
            (string) value from config
        
        Raises:
            XmlConfigParserException: when both argument category and default category are unspecified
            KeyError: when category or key was not found
            
        """
        if category is None:
            category = self.defaultCategory

        if category is None:
            raise XmlConfigParserException("Both argument category and default category are unspecified!")

        return self.cfg[category][key]
    

    def getBool(self, key, category=None):
        """get value for key from config and convert to BOOL - see get() for more details"""
        return True if (self.get(key, category) != "False") else False


    def getInt(self, key, category=None):
        """get value for key from config and convert to INT - see get() for more details"""
        return int(self.get(key, category))
    

    def set(self, value, key, category=None):
        """default setter method to set value for key in config

        Args:
            value (string): value to set
            key (string): key to find in config
            category (string): category to look for key in, when unsfecified use self.defaultCategory

        Raises:
            XmlConfigParserException: when both argument category and default category are unspecified
            KeyError: when category was not found
            
        """
        if category is None:
            category = self.defaultCategory

        if category is None:
            raise XmlConfigParserException("Both argument category and default category are unspecified!")

        self.cfg[category][key] = value
    

    def getCategory(self, category):
        """get whole category of keys and values as dict - useful to pass multiple values to function"""
        return self.cfg[category]
    

    def getCfgDict(self):
        """get whole config of categories as dict of dicts"""
        return self.cfg


    def getRoot(self):
        """get root of xml config file"""
        return self.root
