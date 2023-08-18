from models import  Model

# Should re-save with filled in missing fields.
models = Model.load_from_file('../static_data/models.json')
Model.save_to_file(models, '../static_data/models.json')