import setuptools

if __name__ == "__main__":
    from importlib.util import find_spec
    if find_spec("PySide6"): print("Found PySide6")
    if find_spec("requests"): print("Found requests")
    if find_spec("dotenv"): print("Found dotenv")

setuptools.setup(
    name='pcgs-inv-gui',
    version='0.1a0',
    url='https://github.com/bobdafett/pcgs-inv-gui',
    install_requires=[
        'requests',
        'msal',
        'PySide6',
        'dotenv'
    ],
    author='Lucas Vas',
    author_email='lvas463@gmail.com',
    description='PCGS Coin Inventory'
)
