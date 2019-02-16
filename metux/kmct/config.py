import yaml
from util import set_from, dict_from, dict_keys_from, dict_merge

class Feature:
    def __init__(self, name, cf, source):
        if cf is None:
            cf = {}

        self.name   = name
        self.cf     = cf
        self.source = source

    def get_kconf_enable(self):
        return set_from(self.cf, 'kconf-enable')

    def get_kconf_module(self):
        return set_from(self.cf, 'kconf-module')

    def get_kconf_setting(self):
        return dict_from(self.cf, 'kconf-setting')

    def get_feature_enable(self):
        return set_from(self.cf, 'feature-enable')

    def get_kconf_all(self):
        return (set_from(self.cf, 'kconf-enable')
               |set_from(self.cf, 'kconf-module')
               |dict_keys_from(self.cf, 'kconf-setting'))

class Rule:
    def __init__(self, name, cf, source):
        self.name = name
        self.cf = cf
        self.source = source

    def get_on_feature(self):
        return set_from(self.cf, 'on-feature')

    def get_feature_enable(self):
        return set_from(self.cf, 'feature-enable')

class Config:
    def __init__(self, config_dir, name):
        self.config_dir = config_dir
        self.name = name
        self.imports = {}
        self.features = {}
        self.rules = []

        fn = config_dir+"/"+name+".yml"
        with open(fn) as f:
            self.cf = yaml.safe_load(f)

        if self.cf is None:
            raise Exception("failed loading config file: %s" % fn)

        # process imports
        if 'import' in self.cf:
            for i in self.cf['import']:
                self.imports[i] = Config(config_dir, i)

        # process features
        if 'features' in self.cf:
            for fname in self.cf['features']:
                self.features[fname] = Feature(fname, self.cf['features'][fname], self.name)

        # process rules
        if 'rules' in self.cf:
            for rule in self.cf['rules']:
                self.rules.append(Rule(None, rule, self.name))

    def get_recursive_set(self, name):
        lst = set_from(self.cf, name)
        for i in self.imports:
            lst |= self.imports[i].get_recursive_set(name)
        return lst

    def get_recursive_dict(self, name):
        lst = dict_from(self.cf, name)
        for i in self.imports:
            dict_merge(lst, self.imports[i].get_recursive_dict(name))
        return lst

    def get_kconf_all(self):
        allconf = (set_from(self.cf, 'kconf-enable')
                  |set_from(self.cf, 'kconf-module')
                  |dict_keys_from(self.cf, 'kconf-setting'))

        for x in self.features:
            allconf |= self.features[x].get_kconf_all()

        for x in self.imports:
            allconf |= self.imports[x].get_kconf_all()

        return allconf

    def get_kconf_enable(self):
        return self.get_recursive_set('kconf-enable')

    def get_kconf_module(self):
        return self.get_recursive_set('kconf-module')

    def get_kconf_setting(self):
        return self.get_recursive_dict('kconf-setting')

    def get_feature_enable(self):
        return self.get_recursive_set('feature-enable')

    """retrieve a feature object by name"""
    def get_feature(self, name):
        if name in self.features:
            return self.features[name]

        for iname in self.imports:
            f = self.imports[iname].get_feature(name)
            if f is not None:
                return f

    """retrieve list of feature objects in this conf and all imported ones"""
    def get_all_features():
        flist = self.features
        for iname, iconfig in self.imports.iteritems():
            for fname, feature in iconfig.get_all_features():
                if fname not in flist:
                    flist[fname] = feature
        return flist

    """retrieve list of rule objects in this conf and all imported ones"""
    def get_all_rules(self):
        rlist = self.rules
        for iname, iconfig in self.imports.iteritems():
            rlist += iconfig.get_all_rules()
        return rlist
