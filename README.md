# TRON REST

TRON Rest is a microservice for getting TRON account resources written in Python FastAPI

## Installation

Just clone the repo and use Docker Compose utility

```bash
docker compose up --build
```

## Usage
GET:
```
/info/?limit=0&offset=0
```
- limit (optional) - number of transactions to get
- offset (optional) - start number

*If these parameters are not set, you'll get all transactions*

POST:
```
/info/{ADDRESS}
```
- ADDRESS - TRON account address in base58 format

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPL-3.0 license](https://choosealicense.com/licenses/gpl-3.0/)
