import json

class Model:
    def __init__(self, ID, HF_ID, URL, SIZE, LICENSE, ALIASES=[]):
        self.ID = ID
        self.HF_ID = HF_ID
        self.URL = URL
        self.SIZE = SIZE
        self.LICENSE = LICENSE
        self.ALIASES = ALIASES

    @classmethod
    def from_dict(cls, model_dict):
        """Create a Model instance from a dictionary."""
        # If 'ALIASES' key is not present, it defaults to an empty list
        return cls(
            ID=model_dict['ID'],
            HF_ID=model_dict['HF_ID'],
            URL=model_dict['URL'],
            SIZE=model_dict['SIZE'],
            LICENSE=model_dict['LICENSE'],
            ALIASES=model_dict.get('ALIASES', [])
        )

    def to_dict(self):
        """Convert the Model instance to a dictionary."""
        return {
            'ID': self.ID,
            'HF_ID': self.HF_ID,
            'URL': self.URL,
            'SIZE': self.SIZE,
            'LICENSE': self.LICENSE,
            'ALIASES': self.ALIASES
        }

    @classmethod
    def load_from_file(cls, filename):
        """Load a list of Model instances from a JSON file."""
        with open(filename, 'r') as f:
            models_list = json.load(f)
        return [cls.from_dict(model_dict) for model_dict in models_list]

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
        """Save a list of Model instances to a JSON file."""
        # Sort the models by their ID
        sorted_models = sorted(models, key=lambda model: model.ID)
        with open(filename, 'w') as f:
            json.dump([model.to_dict() for model in sorted_models], f, indent=4)