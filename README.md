# Sophists official Website

It mainly uses django, ignore as repo is showing as javascript, this is because the project is not using any cdn, in static i am using entire javascript files

## Installation

1. Create a virtual env

```bash
virtualenv myenv

myenv\Scripts\activate
```
2. Install all the requirements

```bash
pip install -r requirements.txt
```
3. Make migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run server
```bash
python manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
