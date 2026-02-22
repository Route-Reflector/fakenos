# Installation

## PyPi (Recommended)
FakeNOS has been published in PyPi. To install it using `pip` just run the following command
```bash
python3 -m pip install fakenos
```

## Git
The following methods are not recommended unless you are doing development. If this is the case, then we recommend following the `uv` method, as it has all the features and will make your development process easier.

### Using pip
Before installing this way, you need to download and install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). If you have already installed `git` just run the following command:
```bash
python3 -m pip install git+https://github.com/dmulyalin/fakenos
```

# Using uv (Recommended for dev)
FakeNOS uses [uv](https://docs.astral.sh/uv/) to manage dependencies and
virtual environments. Follow steps below to install FakeNOS using uv:

```{ .bash .annotate }
curl -LsSf https://astral.sh/uv/install.sh | sh # (1)
git clone https://github.com/fakenos/fakenos     # (2)
cd fakenos                                       # (3)
uv sync                                         # (4)
```

1.  Install uv
2.  Clone FakeNOS repository from GitHub master branch
3.  Navigate to fakenos folder
4.  Run uv to create virtual environment and install dependencies
