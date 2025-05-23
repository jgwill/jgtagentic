import re
#jgtagentic/__init__.py
def bump_version(version):
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

with open('jgtagentic/__init__.py', 'r') as file:
    package_init_content = file.read()

version_match = re.search(r"version=['\"]([^'\"]*)['\"]", package_init_content)
if version_match:
    current_version = version_match.group(1)
    new_version = bump_version(current_version)
    new_package_init_content = re.sub(r"version=['\"]([^'\"]*)['\"]", f"version='{new_version}'", package_init_content)

    with open('jgtagentic/__init__.py', 'w') as file:
        file.write(new_package_init_content)
    
    #Also patch pyproject.toml
    with open('pyproject.toml', 'r') as file:
        pyproject_content = file.read()
    pyproject_content = re.sub(r"version = \"(.*)\"", f"version = \"{new_version}\"", pyproject_content)
    with open('pyproject.toml', 'w') as file:
        file.write(pyproject_content)
    
    #Also patch package.json
    with open('package.json', 'r') as file:
        package_json_content = file.read()
    package_json_content = re.sub(r"\"version\": \"(.*)\"", f"\"version\": \"{new_version}\"", package_json_content)
    with open('package.json', 'w') as file:
        file.write(package_json_content)
    
    print(new_version)
else:
    raise ValueError("Version string not found in setup.py")