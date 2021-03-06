# xml-config-parser
Python module that parses XML config files with defined structure.  


## Example

Xml file:
```
<?xml version="1.0" encoding="utf8"?>
<configuration>
    <basicConfig>
        <optionalOption>Value</optionalOption>
        <requiredOption>Value</requiredOption>
    </basicConfig>
    <nextConfig>
        <bool>False</bool>
        <whatever>WUBBA LUBA DUB-DUB</whatever>
    </nextConfig>
</configuration>
```

Python code:
```
from xmlConfigParser import XmlConfigParser

# NOTE: specify config options like this 
# NOTE: options with "None" as default value are required
# NOTE: sections with no required options are optional:
cfgValues = {
    "basicConfig": {
        "optionalOption": "default_value",
        "requiredOption": None
    },
    "nextConfig": {
        "bool": "True",
        "whatever": None
    },
    "optionalConfigSection": {
        "opt1": "def_val1",
        "opt2": "def_val2"
    }
}

cfg = XmlConfigParser(cfgValues, "/path/to/xml/config", "basicConfig")

# HACK: you can write your custom conditions and mess with default values and their optionality\
                                                            before you run parseXmlConfig()
# if /optionalConfigSection is present: set default value for /nextConfig/whatever
if not cfg.getRoot().find("basicConfig") is None:
    cfg.set("new_value", "whatever", "nextConfig")
# HACK: this makes /nextConfig/whatever optional

# NOTE: parseXmlConfig will raise XmlConfigParserException if any of required options are missing
cfg.parseXmlConfig()

# returns value of "whatever" from "nextConfig" section
someValue = cfg.get("whatever", "nextConfig")

# converts to bool value of "bool" from "nextConfig" section
boolValue = cfg.getBool("bool", "nextConfig")

# returns value of "whatever" from default section specified in constructor
someOtherValue = cfg.get("optionalOption")

```

## Dependencies
`xml` python library.  
You can install this dependency using `pip`
