import os
import yaml

# Define the directory containing Helm values files
VALUES_DIR = "cicd/chart/"
COMMON_FILE = os.path.join(VALUES_DIR, "common.yaml")

def load_yaml(file_path):
    """Load YAML file and return dictionary (returns empty dict if file is empty)."""
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found.")
        return {}
    
    with open(file_path, "r") as f:
        data = yaml.safe_load(f) or {}
    
    print(f"\nContents of {file_path}:")
    print(yaml.dump(data, default_flow_style=False))
    
    return data

def merge_yaml_files():
    """Merge common.yaml with all values-<env>.yml files and print the results."""
    # Load common.yaml
    common_data = load_yaml(COMMON_FILE)

    # Iterate over all environment-specific YAML files (values-<env>.yml)
    for file in os.listdir(VALUES_DIR):
        if file.startswith("values-") and file.endswith(".yml") and file != "common.yaml":
            env_name = file.replace("values-", "").replace(".yml", "")
            env_file = os.path.join(VALUES_DIR, file)
            output_file = os.path.join(VALUES_DIR, f"merge-values-{env_name}.yml")

            # Load environment-specific values
            env_data = load_yaml(env_file)

            # Merge environment values (overrides common values)
            merged_data = {**common_data, **env_data}

            # Write merged values to a new file
            with open(output_file, "w") as f:
                yaml.dump(merged_data, f, default_flow_style=False)

            # Print merged content
            print(f"\nMerged values for {env_name}:")
            print(yaml.dump(merged_data, default_flow_style=False))

            print(f"✅ Merged file created: {output_file}")

if __name__ == "__main__":
    merge_yaml_files()
