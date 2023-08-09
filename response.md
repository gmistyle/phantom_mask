# Introduction
> These Project focused on showing my usual project structure and coding style. 

I usually build project in three part : `Blueprint, Database, Service`.

- `Blueprint` : Contains many Flask router object. one or multiple service(s) will be utilized in one router. the API response is composed by the service(s) return.
- `Database` : Contains Table Schema object, sqlalchemy engine, DAO (not using orm). I choose to build my own Data Access Object because it is more easy and flexible for myself to achieve my goal to finish a Query.
- `Service` : All feature logic and functionalities.

## A. Required Information
### A.1. Requirement Completion Rate
- [x] List all pharmacies open at a specific time and on a day of the week if requested.
  - Implemented at API: `GET {base_url}/api/v1/pharmacies/opening_hour`.
- [x] List all masks sold by a given pharmacy, sorted by mask name or price.
  - Implemented at API: `GET {base_url}/api/v1/pharmacies/{pharmacy_id}/masks`.
- [x] List all pharmacies with more or less than x mask products within a price range.
  - Implemented at API: `GET {base_url}/api/v1/pharmacies/mask_price`.
- [x] The top x users by total transaction amount of masks within a date range.
  - Implemented at API: `GET {base_url}/api/v1/transactions/summary`.
- [x] The total number of masks and dollar value of transactions within a date range.
  - Implemented at API: `GET {base_url}/api/v1/transactions/summary`.
- [x] Search for pharmacies or masks by name, ranked by relevance to the search term.
  - Implemented at API: `GET {base_url}/api/v1/pharmacies/names`.
  - Implemented at API: `GET {base_url}/api/v1/masks/names`.
- [x] Process a user purchases a mask from a pharmacy, and handle all relevant data changes in an atomic transaction.
  - Implemented at API: `POST {base_url}/api/v1/transactions`.

### A.2. API Document

API LINK: [go here](https://pharmacymask.docs.apiary.io/#).

### A.3. Import Data Commands

```bash
$ python3 import_source_data_script.py
```