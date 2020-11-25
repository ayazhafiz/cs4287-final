import yaml
import os
import glob
import sys


def gen_env(language, description):
    return f"""
ENV RUN_LANG_UBUNTU="18.04"
ENV RUN_LANG_WHICH="{language}"
ENV RUN_LANG_WHICH_DESCRIPTION="{description}"
""".strip()


def run_block(cmds):
    return '\n'.join(map(lambda cmd: f"RUN {cmd}", cmds))


def gen_dockerfile(language, description, cmd_pre_install_packages,
                   cmd_install_packages, cmd_post_install_packages):
    return f"""
# Generated Dockerfile, do not modify directly!
# Modify `dockergen.yaml` and run
#   `python images/dockergen.py` in the root directory.
FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

{gen_env(language, description)}

# Service setup
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get update && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

RUN apt-get install -y python3.7 python3-pip
COPY run_lang/requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

# Pre-install
{run_block(cmd_pre_install_packages)}

# Package install
{run_block(cmd_install_packages)}

# Post-install
{run_block(cmd_post_install_packages)}

# Service setup
COPY run_lang /run_lang
COPY start_run_lang.sh /start_run_lang.sh
COPY images/{language}/packages /packages

WORKDIR /

CMD ["./start_run_lang.sh"]
""".lstrip()


def gen_image(path, language):
    with open(os.path.join(path, 'imagegen.yaml')) as fi:
        data = yaml.load(fi, Loader=yaml.FullLoader)
    description = data["description"]
    cmd_pre_install_packages = data["pre_install_pkg"].strip().split('\n')
    cmd_post_install_packages = data["post_install_pkg"].strip().split('\n')

    install_package_cmd = data["install_pkg_command"].strip()
    packages = data["ecosystem_pkg"]
    cmd_install_packages = list(
        map(lambda pkg: f"{install_package_cmd} {pkg}", packages))

    dockerfile = gen_dockerfile(
        language=language,
        description=description,
        cmd_pre_install_packages=cmd_pre_install_packages,
        cmd_post_install_packages=cmd_post_install_packages,
        cmd_install_packages=cmd_install_packages)
    with open(os.path.join(path, 'Dockerfile'), 'w') as fi:
        fi.write(dockerfile)
    with open(os.path.join(path, "packages"), "w") as fi:
        fi.write('\n'.join(packages))


if not os.path.exists('images/'):
    print("Please run at the repo root.", file=sys.stderr)
    sys.exit(1)

for path in glob.glob('images/*/'):
    language = os.path.relpath(path, 'images/')
    print(f"Generating \"{language}\"...")
    gen_image(path, language)

print("All done.")
