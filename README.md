# E-Commerce Grocery Store

This is a Flask-based grocery store where users can browse products, add items to the cart, and make purchases. It uses SQLite to store product details, user information, and order history. The app provides a simple and smooth shopping experience with essential features like cart management and checkout. 🚀

**Note**: This Project is made using [UV](https://github.com/astral-sh/uv)


To run this please install UV 

## On macOS and Linux.
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
## On Windows.
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```


Or, from PyPI:

## With pip.
```
pip install uv
```

## Or pipx.
```
pipx install uv
```

If installed via the standalone installer, uv can update itself to the latest version:

```
uv self update
```


## For Running the application

```
# Clone the repository

git clone https://github.com/ankitkhushwaha/grocerystore.git

cd grocerystore

uv run main.py

```