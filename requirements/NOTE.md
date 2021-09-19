# Add --use-deprecated to the requirements file parser

> Default pip has't the ability to parse `--use-deprecated` from requirements file.
But `lxml`, `numpy` or `pandas` will never finish building on my ubuntu in wsl 😶

#
### Modify local pip in this fragment [(github/pypa/pip)](https://github.com/pypa/pip/blob/4f4c310e989ea6101cf9dd7d6156d6fdc652e9f6/src/pip/_internal/req/req_file.py#L61)


```
# options to be passed to requirements
SUPPORTED_OPTIONS_REQ: List[Callable[..., optparse.Option]] = [
    cmdoptions.install_options,
    cmdoptions.global_options,
    cmdoptions.hash,
]
```

### Jump into <MY_LOCAL_VENV>/lib64/python3.10/site-packages/pip/_internal/req/req_file.py
```python
# find this code (~ on line:60)
SUPPORTED_OPTIONS_REQ: List[Callable[..., optparse.Option]] = [
    cmdoptions.install_options,
    cmdoptions.global_options,
    cmdoptions.hash,
    cmdoptions.use_deprecated_feature,  # <-- and add this line
]
```
