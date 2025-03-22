import os
import yaml

# Define absolute paths
REPO_ROOT = os.getcwd()  # Get the root directory of the repository
COMMON_FILE = os.path.join(REPO_ROOT, "common.yml")
VALUES_DIR = os.path.join(REPO_ROOT, "cicd/charts/")

def load_yaml(file_path):
    """Load YAML file and return dictionary (returns empty dict if file is empty)."""
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found.")
        return {}

    with open(file_path, "r") as f:
        data = yaml.safe_load(f) or {}

    print(f"\n📂 Contents of {file_path}:")
    print(yaml.dump(data, default_flow_style=False))

    return data

def merge_yaml_files():
    """Merge common.yaml with all values-<env>.yml files and print the results."""
    
    print(f"🔍 Checking for files in: {VALUES_DIR}")  

    # Check if common.yaml exists
    if not os.path.exists(COMMON_FILE):
        print(f"❌ ERROR: Common file '{COMMON_FILE}' not found!")
        return

    # Load common.yaml
    common_data = load_yaml(COMMON_FILE)

    # Check if /cicd folder exists
    if not os.path.exists(VALUES_DIR):
        print(f"❌ ERROR: Directory '{VALUES_DIR}' does not exist!")
        return

    found_values_files = False  # Flag to check if any values file exists

    # Iterate over all environment-specific YAML files (values-<env>.yml)
    for file in os.listdir(VALUES_DIR):
        if file.startswith("values-") and file.endswith(".yml"):
            found_values_files = True  # Found at least one values file
            env_name = file.replace("values-", "").replace(".yml", "")
            env_file = os.path.join(VALUES_DIR, file)
            output_file = os.path.join(VALUES_DIR, f"merge-values-{env_name}.yml")

            # Check if environment file exists
            if not os.path.exists(env_file):
                print(f"❌ ERROR: Environment file '{env_file}' not found! Skipping...")
                continue  # Skip this file and continue

            # Load environment-specific values
            env_data = load_yaml(env_file)

            # Merge environment values (overrides common values)
            merged_data = {**common_data, **env_data}

            # Write merged values to a new file
            with open(output_file, "w") as f:
                yaml.dump(merged_data, f, default_flow_style=False)

            # Print merged content
            print(f"\n✅ Merged values written to: {output_file}")
            print(f"\n📂 Merged contents of {output_file}:")
            print(yaml.dump(merged_data, default_flow_style=False))

    if not found_values_files:
        print(f"❌ ERROR: No 'values-<env>.yml' files found in {VALUES_DIR}!")

if __name__ == "__main__":
    merge_yaml_files()
