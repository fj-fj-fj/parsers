# tree .

<pre>
requirements
├── README.md
├── apt
│   ├── <a href="./apt/base.txt">./base.txt</a> (build python dependencies)
│   ├── <a href="./apt/optional.txt">./optional.txt</a> (file and code analysis)
│   └── <a href="./apt/pip.txt">./pip.txt</a> (pip required)
└── pip
    ├── <a href="./pip/base.txt">./base.txt</a> (build project requirements)
    ├── <a href="./pip/lint.txt">./lint.txt</a> (style,types,guard, etc)
    └── <a href="./pip/local.txt">./local.txt</a> (base + lint)

2 directories, 7 files
</pre>

## install apt requirements with [apt_install.sh](../scripts/apt_install.sh)
```bash
cd $PROJECT_DIR
sudo apt update && ./scripts/apt_install.sh
```

## install pip requirements

### Determine if Python is running inside virtualenv
```bash
# check whether sys.prefix == sys.base_prefix
python -c 'import sys; print(sys.prefix == sys.base_prefix)'
# If True, you are not in a virtual environment
# if False, you are
# Inside a virtual environment, sys.prefix points to the virtual environment
# sys.base_prefix is the prefix of the system Python the virtualenv was created from
# if False, activate your virtualenv:
# with Direnv
mv $PROJECT_DIR/.envrc.samvle $PROJECT_DIR/.envrc
direnv allow .
# or vanile
python -m venv $PROJECT_DIR/../.venv
$PROJECT_DIR/../.venv/bin/activate
```

```bash
# install base reqs
pip install -r requirements.txt

# or install dev reqs
pip install -r requirements/pip/local.txt
```
