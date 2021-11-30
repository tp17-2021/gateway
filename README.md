# Gateway

All Gateway services can be started from this single repository with docker-compose.

At the moment, `docker-compose.yml` composes two containers (Voting Service and Mongo DB for Vote DB model) and binds ports `8222` and `8223`.

#### Submodules

This repository makes use of GitHub submodules, which provides some kind of linking other repositories into this one as directories. Every gateway service's repository is linked here to a similarly named directory.

Each submodule references certain commit in remote repository, so ```git submodule update``` is needed after every remote repository change to take effect here.

When cloning a repository with submodules, use `--recurse-submodules` to clone submodules too. Otherwise, submodules won't be cloned and the directories will be empty. The same applies to `git pull`.


##### Submodules can be tricky

In order to develop a Gateway component in its own repository but with the ability to test run it during the process with ```docker-compose.yml``` in order to be able to communicate other components, one must do the development inside submodule directory inside supermodule (gateway repo). Content of each submodule directory is a standalone git repository. But, after clone of the supermodule, submodules are checked out to a speciffic commit. In order to develop in the submodule, checkout your branch _inside the submodule_.

```bash
cd my-submodule
git checkout development
```

When working with git, make sure you are in the submodule's directory when you want to use git for a submodule or you are in the supermodule directory when you want to use git for it instead.

In order to push new commits from the submodule, some origin url tweaking is required to use `git+ssh` if you mind typing in your `username` and `password`.


## Requirements

`docker-compose.yml` uses version `"3.8"`, which means that required versions are: `docker >= 19.03.0` and `docker-compose >= 1.25.5`.

Installed versions can be checked with `docker -v` and `docker-compose -v`.


## Usage

Clone this repository with:

```bash
git clone --recurse-submodules https://github.com/tp17-2021/gateway.git
```

Navigate inside the `gateway` folder and run:

```bash
docker-compose up -d --build
```

Containers should be running. You can check by `docker ps -a` or by navigating to `localhost:8222/docs` which should show FastAPI docs webpage for `voting-service`.

---

It's possible to checkout a different branch and run docker-compose from there. Practical example would be including a new submodule to the composition and wanting to test its integration with the rest while the new component isn't included in the main branch of gateway repository but is already included in the development branch. For example, run following commands to compose a development version of Gateway with the new submodule:

```bash
git clone --recurse-submodules https://github.com/tp17-2021/gateway.git
cd gateway
git checkout development
git pull --recurse-submodules
docker-compose up -d --build
```

---

Submodules' directories behave as normal git repositories, so it's possible to checkout certain branches or even commits in submodules. This is useful when non-main version of submodule is needed. Docker-compose uses submodule's Dockerfile present in a directory at the moment of composing.

Let's say we want to specifically use development branch of voting-service. To do that, use following.

```bash
git clone --recurse-submodules https://github.com/tp17-2021/gateway.git
cd gateway
cd voting-service
git checkout development
cd ..
docker-compose up -d --build
```
