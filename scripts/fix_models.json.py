from models import  Model

resave = True
print_duplicates = True

# Should re-save with filled in missing fields.
models = Model.load_from_file('../static_data/models.json')
if(resave):
    Model.save_to_file(models, '../static_data/models.json')

if(print_duplicates):
    from collections import defaultdict

    # Create a dictionary to store the count of each ID
    id_counts = defaultdict(int)

    # Increment the count for each ID
    for model in models:
        id_counts[model.ID] += 1

    # Filter out IDs that appear more than once
    duplicate_ids = [id_ for id_, count in id_counts.items() if count > 1]

    # Get the Model objects that have duplicate IDs
    duplicate_models = [model for model in models if model.ID in duplicate_ids]

    # Print out the duplicate Model objects
    for model in duplicate_models:
        print(f"ID: {model.ID}, HF_ID: {model.HF_ID}, URL: {model.URL}, SIZE: {model.SIZE}, LICENSE: {model.LICENSE}")