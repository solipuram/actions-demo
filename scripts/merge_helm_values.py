import os
import yaml
from collections import OrderedDict

# Define absolute paths
REPO_ROOT = os.getcwd()  # Get the root directory of the repository
COMMON_FILE = os.path.join(REPO_ROOT, "common.yaml")
VALUES_DIR = os.path.join(REPO_ROOT, "cicd/charts")  # Updated path

# Custom Dumper to preserve order
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def load_yaml(file_path):
    """Load YAML file and return dictionary (preserving order)."""
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found.")
        return OrderedDict()  # Use OrderedDict to maintain order

    with open(file_path, "r") as f:
        data = yaml.safe_load(f) or OrderedDict()

    print(f"\n📂 Contents of {file_path}:")
    print(yaml.dump(data, default_flow_style=False, sort_keys=False))

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

    # Check if /cicd/charts/ folder exists
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

            # Merge environment values (overrides common values), keeping order
            merged_data = OrderedDict()
            merged_data.update(common_data)  # Keep original order from common.yaml
            merged_data.update(env_data)  # Override with env-specific values

            # Write merged values to a new file, preserving order
            with open(output_file, "w") as f:
                yaml.dump(merged_data, f, default_flow_style=False, sort_keys=False, Dumper=NoAliasDumper)

            # Print merged content
            print(f"\n✅ Merged values written to: {output_file}")
            print(f"\n📂 Merged contents of {output_file}:")
            print(yaml.dump(merged_data, default_flow_style=False, sort_keys=False, Dumper=NoAliasDumper))

    if not found_values_files:
        print(f"❌ ERROR: No 'values-<env>.yml' files found in {VALUES_DIR}!")

if __name__ == "__main__":
    merge_yaml_files()
