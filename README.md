# Fake Site Scrapper

## Run App
### Local

```sh
$ sh run.sh
```

```sh
$ poetry run python -m app.main
```


## The scraping result will be saved in a file

``` 
 job_items.parquet
```

This file contains current vacancies. You can read it using the website:

- [https://www.parquet-viewer.com/#parquet-online](https://www.parquet-viewer.com/#parquet-online)

## Development
### Run Tests and Linter

```
$ poetry run tox
```
