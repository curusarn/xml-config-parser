import xml.etree.ElementTree


class XmlConfigParserException(Exception):
    pass


class XmlConfigParser():
    # saves default cfgValues and validates xmlFiles
    def __init__(self, cfgValues, xmlFile, cat=None):
        self.cfg = cfgValues
        self.root = xml.etree.ElementTree.parse(xmlFile).getroot() 
        self.defaultCategory = cat
        
        if self.root is None:
            raise XmlConfigParserException("Xml is malformed - can't find root")


    # @brief iterates trough cfgValues and looks for apropriate keys in xmlFile
    # treats already present values as defaults and overrides them
    # @return number of parsed keys - might be useful for someone
    def parseXmlConfig(self, verbious=False):
        count = 0
        for section, cfg in self.cfg.items():
            if verbious:
                print("CAT: {0} config:".format(section))
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


    # get BOOL value from config
    def getBool(self, key, category=None):
        if category is None:
            category = self.defaultCategory
        return True if (self.cfg[category][key] != "False") else False


    # get INT value from config
    def getInt(self, key, category=None):
        if category is None:
            category = self.defaultCategory
        return int(self.cfg[category][key])


    # get (STRING) value from config
    # method is called get() not getString() because no conversion is applied 
    def get(self, key, category=None):
        if category is None:
            category = self.defaultCategory
        return self.cfg[category][key]
    

    # set (STRING) value to config
    # use with caution
    def set(self, value, key, category=None):
        if category is None:
            category = self.defaultCategory
        self.cfg[category][key] = value
    

    # returns whole cfg category - useful to pass multiple values to function
    def getCategory(self, category):
        return self.cfg[category]
    

    # returns whole cfg dict
    def getCfgDict(self):
        return self.cfg


    # returns xml root of xmlFile structure
    # use with caution 
    def getRoot(self):
        return self.root


