import json

class Model:
    def __init__(self, ID, HF_ID, URL, SIZE):
        self.ID = ID
        self.HF_ID = HF_ID
        self.URL = URL
        self.SIZE = SIZE

    @classmethod
    def from_dict(cls, model_dict):
        """Create a Model instance from a dictionary."""
        return cls(
            ID=model_dict['ID'],
            HF_ID=model_dict['HF_ID'],
            URL=model_dict['URL'],
            SIZE=model_dict['SIZE']
        )

    def to_dict(self):
        """Convert the Model instance to a dictionary."""
        return {
            'ID': self.ID,
            'HF_ID': self.HF_ID,
            'URL': self.URL,
            'SIZE': self.SIZE
        }

    @classmethod
    def load_from_file(cls, filename):
        """Load a list of Model instances from a JSON file."""
        with open(filename, 'r') as f:
            models_list = json.load(f)
        return [cls.from_dict(model_dict) for model_dict in models_list]

    @staticmethod
    def save_to_file(models, filename):
        """Save a list of Model instances to a JSON file."""
        with open(filename, 'w') as f:
            json.dump([model.to_dict() for model in models], f, indent=4)