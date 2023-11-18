from src.species import Species
import json


def find_source_object(object_dict):
    source_key = []
    for key, subdict in object_dict.items():
        if "source" in subdict:
            if subdict["source"]:
                source_key.append(key)
                #return key
    if len(source_key) > 1:
        raise ValueError("Currently we only support single-source system. Please make sure you only have one source.")
    elif len(source_key) == 1:
        return source_key[0]
    else:
        raise ValueError("No source found.")


class DefaultFields:
    _instance = None

    celest = None
    species = None
    int_spec = None
    therm_spec = None

    def __new__(cls):
        if cls._instance is None:
            cls._get_default_objects(cls)
            cls._get_default_parameters(cls)
            cls._instance = object.__new__(cls)
        return cls._instance

    def _get_default_objects(self):
        with open('resources/objects.json', 'r') as f:
            #data = f.read().splitlines(True)
            #self.celest = json.loads(data[["Jupiter (Europa-Source)" in s for s in data].index(True)])
            systems = json.load(f)
            self.celest = [objects for condition, objects in zip([s['SYSTEM-NAME']=='Jupiter (Europa-Source)' for s in systems], systems) if condition][0]

    def _get_default_parameters(self):
        self.species = {}
        with open('resources/input_parameters.txt') as f:
            data = f.read().splitlines(True)
            self.int_spec = json.loads(data[["integration_specifics" in s for s in data].index(True)])["integration_specifics"]
            self.therm_spec = json.loads(data[["thermal_evap_parameters" in s for s in data].index(True)])[
                "thermal_evap_parameters"]
            for k, v in json.loads(data[-1]).items():
                self.species[f"{k}"] = Species(**v)

        source_key = find_source_object(self.celest)
        source_index = list(self.celest).index(source_key)
        self.int_spec["source_index"] = source_index
        if source_index > 2:    # Also includes SYSTEM-NAME
            self.int_spec["moon"] = True
        else:
            self.int_spec["moon"] = False

    @classmethod
    def change_defaults(cls, **kwargs):
        cls.int_spec = kwargs.get("int_spec", cls.int_spec)
        cls.therm_spec = kwargs.get("therm_spec", cls.therm_spec)
        cls.celest = kwargs.get("celest", cls.celest)
        cls.species = kwargs.get("species", cls.species)
        cls.num_species = len(cls.species)


class Parameters:
    """
    Parameter singleton class.
    All variables are class wide and are assigned at first instance creation.
    Class-methods allow for the modification of the parameters. These get called by the 'NewParams' class (see below).
    """
    _instance = None

    int_spec = {}
    therm_spec = {}
    celest = None
    species = {}
    num_species = 0

    def __new__(cls):
        """
        Assigns default values using the 'Default Fields' class.
        Only (re-)assigns variables if the '_instance' class variable is 'None'. This is only the case for the first
        class instance creation or after parameters were reset using the 'reset' staticmethod.
        """
        if cls._instance is None:
            default = DefaultFields()
            cls.int_spec = default.int_spec
            cls.therm_spec = default.therm_spec
            cls.species = default.species
            cls.celest = default.celest
            cls.num_species = len(cls.species)

            cls._instance = object.__new__(cls)

        return cls._instance

    def __str__(self):
        """
        Modifies how the Parameter class gets printed.
        """
        s = "Integration specifics: \n" + f"\t {self.int_spec} \n"
        s += "Species: \n"
        for i in range(1, self.num_species + 1):
            s += f"\t {i}) " + str(vars(self.species[f"species{i}"])["description"]) + '\n'
            for k in vars(self.species[f"species{i}"]).keys():
                s += "\t \t" + f"{k} : {vars(self.species[f'species{i}'])[k]} \n"
        s += f"Thermal evaporation parameters: \n \t {self.therm_spec} \n"
        s += f"Celestial objects: \n \t {self.celest} \n"
        return s

    def __call__(self):
        return self

    def get_species(self, name=None, id=None, num=None):
        """
        Function to access the species.

        Arguments
        ---------
        name : str      (default: None)
            Name of the desired species.
        id : int        (default: None)
            id of the desired species as defined in src/species.py
        num : int       (default: None)
            Number index of desired species.
        """
        if num is not None:
            return self.species[f"species{num}"]

        elif id is not None:
            for i in range(self.num_species):
                if self.species[f"species{i+1}"].id == id:
                    return self.species[f"species{i+1}"]
            return None

        elif name is not None:
            for i in range(self.num_species):

                if self.species[f"species{i+1}"].name == name:
                    return self.species[f"species{i+1}"]
            return None

        else:
            return

    @classmethod
    def modify_species(cls, *args):
        """
        Overwrite species if args supply species
        """
        if len(args) != 0:
            cls.species = {}
            for index, arg in enumerate(args):
                cls.species[f"species{index + 1}"] = arg
            cls.num_species = len(args)
            print("Species loaded.")

    @classmethod
    def modify_objects(cls, celestial_name=None, object=None, as_new_source=False, new_properties=None):
        """
        Load different set of celestial objects and/or modify existing objects.

        Arguments
        ---------
        celestial_name : str    (default: None)
            Name of the celestial system to load.
        object : str    (default: None)
            Name (key) of the celestial object to be modified.
        as_new_source : bool    (default: False)
            If 'object' is not 'None' and 'as_new_source' is 'True', it will make the object act as new particle source.
        new_properties : dict   (default: None)
            If 'object' is not 'None' and 'new_properties' is not 'None', new rebound.Particle properties will be
            applied to the object.
        """
        if celestial_name is not None:
            with open('resources/objects.json', 'r') as f:
                #saved_objects = f.read().splitlines(True)
                #cls.celest = json.loads(saved_objects[[f"{celestial_name}" in s for s in saved_objects].index(True)])

                systems = json.load(f)
                cls.celest = [objects for condition, objects in
                               zip([s['SYSTEM-NAME'] == f"{celestial_name}" for s in systems], systems) if
                               condition][0]

                source_key = find_source_object(cls.celest)
                source_index = list(cls.celest).index(source_key)
                cls.int_spec["source_index"] = source_index
                if source_index > 2:  # Also includes SYSTEM-NAME
                    cls.int_spec["moon"] = True
                else:
                    cls.int_spec["moon"] = False

        if object is not None:
            if as_new_source:
                source_key = find_source_object(cls.celest)
                del cls.celest[source_key]["source"]
                cls.celest[object]["source"] = True
                print("Globally modified source object.")

            if type(new_properties) == dict:
                cls.celest[object].update(new_properties)

    @classmethod
    def modify_spec(cls, int_spec=None, therm_spec=None):
        """
        Modifies integration specifics or thermal specifics if dictionary with new parameters are provided.
        """
        if int_spec is not None:
            cls.int_spec.update(int_spec)
        if therm_spec is not None:
            cls.therm_spec.update(therm_spec)

    @staticmethod
    def reset():
        """
        Resets the singleton and applies default values.
        """
        Parameters._instance = None
        Parameters()


class NewParams:
    """
    This class allows for modification of the parameter singleton settings.
    In order to apply the changes one needs to call the class initiated.
    """
    def __init__(self, species=None, objects=None, int_spec=None, therm_spec=None, celestial_name=None):
        """
        Set new objects/parameters.

        Arguments
        ---------
        species : <class Species> (can be a list)     (default: None)
            New species instance for the simulation.
            Signature:  Species(name: str, n_th: int, n_sp: int, mass_per_sec: float,
                                duplicate: int, beta: float, lifetime: float, n_e: float, sput_spec: dict)
            If attribute not passed to species, it is either set to 'None' or to default value.
        objects : dict      (default: None)
            Manipulation of existing objects from a system.
            A new source can be defined and object properties can be changed.
            (see rebound.Particle properties - https://rebound.readthedocs.io/en/latest/particles/)
            Example: {'Io': {'source': True, 'm': 1e23, 'a': 3e9}, 'Ganymede': {...}}
        int_spec : dict     (default: None)
            Update integration parameters. Only the specific dict parameter can be passed.
        therm_spec : dict   (default: None)
            Update thermal evaporation parameters. Only the specific dict parameter can be passed.
        celestial_name : str    (default: None)
            Name of the celestial system to be used. Valid are entries from src/objects.txt

        Examples
        --------
        *   newp = NewParams(celestial_name = 'Jupiter (Europa-Source)', objects = {'Io': {'source': True, 'm': 1e23, 'a': 3e9})
            newp()
            --> Loads the 'Jupiter (Europa-Source)' from src/objects.txt, but modifies the mass and semi-major axis of Io,
                and switches from Europa as source to using Io as the particle sourcing object.

        """
        self.species = species
        self.objects = objects  # dictionary of the celestial objects and their properties to be updated
        self.celestial_name = celestial_name
        self.int_spec = int_spec
        self.therm_spec = therm_spec

        Parameters.reset()

    def __call__(self):
        """
        Apply changes by calling the instance.
        """
        Parameters()
        if self.species is not None:
            Parameters.modify_species(*self.species)

        if self.celestial_name is not None:
            Parameters.modify_objects(celestial_name=self.celestial_name)

        if isinstance(self.objects, dict):
            for k1, v1 in self.objects.items():
                if isinstance(v1, dict) and k1 in Parameters.celest:
                    source = v1.pop('source', False)
                    # False if v1 now empty:
                    if v1:
                        Parameters.modify_objects(object=k1, as_new_source=source, new_properties=v1)
                    else:
                        Parameters.modify_objects(object=k1, as_new_source=source)

        if self.therm_spec is not None or self.int_spec is not None:
            Parameters.modify_spec(int_spec=self.int_spec, therm_spec=self.therm_spec)

        return

