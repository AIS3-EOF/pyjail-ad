# Pyjail AD

## Install

```bash
poetry install
```

## Run

```bash
poetry run python -m pyjail_ad.flag_worker &
poetry run python -m pyjail_ad.patch_worker &
poetry run flask --app pyjail_ad.app run
```
