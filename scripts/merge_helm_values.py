import os
import yaml
from collections import OrderedDict

# Define paths
REPO_ROOT = os.getcwd()  # Root directory of repo
COMMON_FILE = os.path.join(REPO_ROOT, "common.yaml")
VALUES_DIR = os.path.join(REPO_ROOT, "cicd/charts")  # Correct path

# Custom Dumper to preserve order
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def load_yaml(file_path):
    """Loads YAML file and returns an OrderedDict to preserve order."""
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found.")
        return OrderedDict()  # Return empty OrderedDict instead of failing

    with open(file_path, "r") as f:
        try:
            data = yaml.safe_load(f) or OrderedDict()
        except yaml.YAMLError as e:
            print(f"❌ YAML Parsing Error in {file_path}: {e}")
            return OrderedDict()

    print(f"\n📂 Successfully loaded: {file_path}")
    return data

def merge_yaml_files():
    """Merges common.yaml with all values-<env>.yml files."""
    
    print(f"🔍 Checking for values files in: {VALUES_DIR}")

    # Ensure common.yaml exists
    if not os.path.exists(COMMON_FILE):
        print(f"❌ ERROR: Missing common.yaml at {COMMON_FILE}!")
        return

    # Load common.yaml
    common_data = load_yaml(COMMON_FILE)

    # Check if directory exists
    if not os.path.exists(VALUES_DIR) or not os.path.isdir(VALUES_DIR):
        print(f"❌ ERROR: Directory '{VALUES_DIR}' does not exist!")
        return

    found_values_files = False  # Track if at least one values file is found

    # Iterate over environment YAML files
    for file in os.listdir(VALUES_DIR):
        if file.startswith("values-") and file.endswith(".yml"):
            found_values_files = True
            env_name = file.replace("values-", "").replace(".yml", "")
            env_file = os.path.join(VALUES_DIR, file)
            output_file = os.path.join(VALUES_DIR, f"merge-values-{env_name}.yml")

            # Ensure the environment file exists
            if not os.path.exists(env_file):
                print(f"❌ ERROR: Missing {env_file}! Skipping...")
                continue

            # Load environment-specific values
            env_data = load_yaml(env_file)

            # Merge environment values (overrides common values)
            merged_data = OrderedDict()
            merged_data.update(common_data)  # Start with common.yaml data
            merged_data.update(env_data)  # Override with env-specific values

            # Write merged data to a new file
            try:
                with open(output_file, "w") as f:
                    yaml.dump(merged_data, f, default_flow_style=False, sort_keys=False, Dumper=NoAliasDumper)

                print(f"✅ Merged values written to: {output_file}")
            except Exception as e:
                print(f"❌ ERROR: Failed to write {output_file}: {e}")

    if not found_values_files:
        print(f"❌ ERROR: No 'values-<env>.yml' files found in {VALUES_DIR}!")

if __name__ == "__main__":
    merge_yaml_files()
