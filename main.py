import subprocess
import inquirer

def get_installed_kernels():
    # Get a list of installed kernels
    command = "rpm -qa kernel --queryformat '%{VERSION}-%{RELEASE}.%{ARCH}\n'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    installed_kernels = result.stdout.split('\n')[:-1]
    return installed_kernels

def remove_kernel(kernel_version):
    # Remove a specified kernel version
    command = f"sudo dnf remove 'kernel-*{kernel_version}' -y"
    subprocess.run(command, shell=True)

def main():
    # Display the list of installed kernel versions
    installed_kernels = get_installed_kernels()

    # Parse and extract only the version part
    version_numbers = [kernel.split('-')[0] for kernel in installed_kernels]

    questions = [
        inquirer.List(
            "kernel",
            message="Select the kernel version to remove:",
            choices=version_numbers,
        ),
        inquirer.Confirm(
            "confirmation",
            message="Are you sure you want to remove the selected kernel?",
            default=False,
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers["confirmation"]:
        kernel_version_to_remove = answers["kernel"]
        # Remove the specified kernel version
        remove_kernel(kernel_version_to_remove)
        print(f"Kernel version {kernel_version_to_remove} has been removed.")
    else:
        print("Operation canceled.")

if __name__ == "__main__":
    main()
