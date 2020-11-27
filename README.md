# RCE - CS 4287 Final

## Packages

### [router](./router)

Package `router` provides a playground that routes code execution requests to
`run_lang` servers.

### [run_lang](./run_lang)

Package `run_lang` provides an API server answering code execution queries.

### [images](./images)

Package `images` provides `run_lang` images for different ecosystems.

## Development

To run a playground locally, you need to (1) stand up some `run_lang` servers
and (2) start the `router` web server.

### (1) Standing up `run_lang` servers

Prebuilt images for python, javascript, and rust are available on docker under
the `ayazhafiz` repository and can be stood up without additional configuration.
For example,

```bash
docker run --name runpython --publish 9001:9000 ayazhafiz/runpython:latest
docker run --name runjavascript --publish 9002:9000 ayazhafiz/runjavascript:latest
docker run --name runrust --publish 9003:9000 ayazhafiz/runrust:latest
```

Mapping a host port to port 9000 in the container is crucial, as this is the
port the container's code execution server listens to.

After standing up the containers, list the addresses by which they can be
accessed from the outside world in [`routes.sh`](./routes.sh).

#### Building `run_lang` images

Images for each language ecosystem supported by the playground can be found in
the subdirectories of [`images`](./images). Each such image is derived from the
[`runlang_base`](./images/runlang_base) image, which describes a common
configuration needed for running the code execution server found in the
[`./run_lang`](`run_lang`) directory.

Do not modify the Dockerfiles of each language ecosystem directly; rather,
modify the `imagegen.yaml` (for example, [see rust's](./images/rust/imagegen.yaml)),
or create a new one for a new language ecosystem, and then run `python3
images/imimagegen.py` in the root of this repository. This generates a
Dockerfile for the language ecosystem and a `packages` file used by the
`run_lang` server during the container's runtime.

An `imagegen.yaml` file looks like:

```yaml
# A description of the language.
description: "python 3.7"

# The command to install packages when building this container.
install_pkg_command: pip3 install

# The packages to install when building this container.
# Must be an array, each entry of which will be appended to `install_pkg_command`
#   and then executed with the docker `RUN` directive.
# For example, the first package in this list generates
#   RUN pip3 install numpy==1.19.4
ecosystem_pkg:
  - numpy==1.19.4
  - pendulum==2.1.2
  - requests==2.25.0

# Docker commands to run before installing packages.
pre_install_pkg:
  - RUN apt-get install -y python3.7 python3-pip

# Docker commands to run after installing packages.
# You may not need this, but the key must be present.
post_install_pkg:
  - RUN echo 0
```

You can also use the [`build_images.sh`](./build_images.sh) script to generate
and build all images in one go, and use `PUSH=true ./build_images.sh` to also
publish the built images to Dockerhub (though you will need to change the
repository organization from `ayazhafiz` if you don't have write access).

Images are also built and published to Dockerhub under `ayazhafiz` on push to
this repo's master branch thanks to [Travis CI](./.travis.yml).

### (2) Standing up the `router` web server

First install the dependencies:

```bash
pip3 install -r router/requirements.txt
```

There are two ways to start the server:

- `./start_router.sh`: This will start a server suitable for production
- `source routes.sh && FLASK_ENV=development FLASK_APP=router flask run --port 8000`:
  this will start a server for use in development, the main nicety being that
  updates to files in [`router`](./router) will be recognized without needing to
  turn down the server.

Now you have a functional playground at [localhost:8000](http://localhost:8000).
