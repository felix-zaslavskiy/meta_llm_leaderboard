import json

class Model:
    def __init__(self, ID, HF_ID, URL, SIZE, LICENSE, ALIASES=[], CONTAMINATED=False):
        self.ID = ID
        self.HF_ID = HF_ID
        self.URL = URL
        self.SIZE = SIZE
        self.LICENSE = LICENSE
        self.ALIASES = ALIASES
        self.CONTAMINATED = CONTAMINATED

    @classmethod
    def from_dict(cls, model_dict):
        """Create a Model instance from a dictionary."""
        return cls(
            ID=model_dict['ID'],
            HF_ID=model_dict['HF_ID'],
            URL=model_dict['URL'],
            SIZE=model_dict['SIZE'],
            LICENSE=model_dict['LICENSE'],
            ALIASES=model_dict.get('ALIASES', []),
            CONTAMINATED=model_dict.get('CONTAMINATED', False)
        )

    def to_dict(self):
        """Convert the Model instance to a dictionary."""
        return {
            'ID': self.ID,
            'HF_ID': self.HF_ID,
            'URL': self.URL,
            'SIZE': self.SIZE,
            'LICENSE': self.LICENSE,
            'ALIASES': self.ALIASES,
            'CONTAMINATED': self.CONTAMINATED
        }

    _cache = {}  # This dictionary will act as a cache for data loaded from files

    @classmethod
    def load_from_file(cls, filename):
        """Load a list of Model instances from a JSON file."""

        # Check if data for the given filename is already cached
        if filename in cls._cache:
            return cls._cache[filename]

        with open(filename, 'r') as f:
            models_list = json.load(f)

        # Convert the dictionaries to Model instances
        instances = [cls.from_dict(model_dict) for model_dict in models_list]

        # Store the list of Model instances in the cache for subsequent calls
        cls._cache[filename] = instances

        return instances

    @classmethod
    def find_by_hf_id(cls, filename, hf_id):
        """Load models from a file and find a model by its HF_ID."""
        models = cls.load_from_file(filename)
        for model in models:
            if model.HF_ID == hf_id:
                return model
        return None

    @classmethod
    def find_by_alias(cls, filename, alias):
        """Load models from a file and find a model by its alias."""
        models = cls.load_from_file(filename)
        for model in models:
            if alias in model.ALIASES:
                return model
        return None

    @staticmethod
    def save_to_file(models, filename):
        """Save a list of Model instances to a JSON file without duplicates."""

        # Sort the models by their ID
        sorted_models = sorted(models, key=lambda model: model.ID)

        unique_models = []
        seen = set()  # Set to keep track of seen models

        for model in sorted_models:
            model_data = json.dumps(model.to_dict(), sort_keys=True)

            if model_data not in seen:
                seen.add(model_data)
                unique_models.append(model)

        with open(filename, 'w') as f:
            json.dump([model.to_dict() for model in unique_models], f, indent=4)