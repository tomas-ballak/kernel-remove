import subprocess
import inquirer

def get_installed_kernels():
    command = "rpm -qa kernel"
    result = subprocess.check_output(command, shell=True, text=True)
    return set(version.split('-')[1] for version in result.strip().split('\n'))

def get_installed_packages(version):
    packages = [
        f"kernel-{version}",
        f"kernel-modules-{version}",
        f"kernel-modules-core-{version}",
        f"kernel-modules-extra-{version}",
        f"kernel-core-{version}",
    ]
    return [pkg for pkg in packages if subprocess.call(f"rpm -q {pkg}", shell=True) == 0]

def delete_selected_packages(selected_packages):
    if not selected_packages:
        print("No packages selected. Nothing will be deleted.")
        return

    confirm = inquirer.confirm("Do you want to delete the selected packages?", default=True)
    if confirm:
        for package in selected_packages:
            subprocess.run(f"sudo dnf remove {package}", shell=True)
        print("Selected packages deleted successfully.")
    else:
        print("No packages were deleted.")

if __name__ == "__main__":
    installed_versions = get_installed_kernels()

    if not installed_versions:
        print("No kernel packages found.")
    else:
        questions = [
            inquirer.Checkbox('selected_packages',
                              message="Select kernel packages to delete:",
                              choices=[f"kernel-{version}" for version in installed_versions],
                              ),
            inquirer.Text('custom_version',
                          message="Enter a specific kernel version (optional, press Enter to skip):",
                          validate=lambda _, x: x.split('.')[-1].isdigit() if x else True,
                          ),
        ]
        answers = inquirer.prompt(questions)

        if answers['custom_version']:
            version_to_delete = answers['custom_version']
        elif answers['selected_packages']:
            version_to_delete = answers['selected_packages'][0].split('-')[1]
        else:
            print("No version selected. Exiting.")
            exit()

        selected_packages = get_installed_packages(version_to_delete)
        delete_selected_packages(selected_packages)
