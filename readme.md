# PyPass Application 

This is an application to store website address, username, and password.

## How To Install

1. pip install -r requirement.txt
2. python -m --help -> to know

## How To Build and Install

1. pip install -r requirement.txt
2. python setup.py bdist_wheel sdist
3. pip install .

## How To Use

#### Get All Command

```bash
python -m pypass --help
```

#### Initialise Database

```bash
python -m pypass init
```

#### Add New Data

```bash
python -m pypass add <username> -p <password> -w <website_url>
```

#### Get Stored Data

```bash
python -m pypass get
```

#### Delete Data

```bash
python -m pypass delete <id>
```

#### Update Data

```bash
python -m pypass update <id> -u <username> -p <password> -w <website>
```

## FAQ

1. How to know the requirement of the command?
   - just use --help parameter after the command name, example:
   ```bash
   python -m pypass <command> --help
   ```

## Future Improvement
- Export and Import.
- Finish Unittesting.
- Making the stored password can be toggled between encrypted and unencrypted.