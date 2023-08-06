# Response
> Since the actual time to develop this project is only about 1 days, I will focus on showing my usual project structure and coding style. At last, I failed to finish them all (data import, encapsulation, some typo fixed) Sorry!

## A. Required Information
### A.1. Requirement Completion Rate
- [x] List all pharmacies open at a specific time and on a day of the week if requested.
  - Implemented at API: `GET {base_url}/api/v1/pharmacies/business_hour`.
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

## Memo : Not done from here below

### A.3. Import Data Commands

```bash
$ python3 source_data_processor.py
```
## B. Bonus Information

>  If you completed the bonus requirements, please fill in your task below.
### B.1. Test Coverage Report

I wrote down the 20 unit tests for the APIs I built. Please check the test coverage report at [here](#test-coverage-report).

You can run the test script by using the command below:

```ruby
bundle exec rspec spec
```

### B.2. Dockerized
Please check my Dockerfile / docker-compose.yml at [here](#dockerized).

On the local machine, please follow the commands below to build it.

```bash
$ docker build --build-arg ENV=development -p 80:3000 -t my-project:1.0.0 .  
$ docker-compose up -d

# go inside the container, run the migrate data command.
$ docker exec -it my-project bash
$ rake import_data:pharmacies[PATH_TO_FILE]
$ rake import_data:user[PATH_TO_FILE]
```

### B.3. Demo Site Url

The demo site is ready on [heroku](#demo-site-url); you can try any APIs on this demo site.

## C. Other Information

### C.1. ERD

My ERD [erd-link](#erd-link).

### C.2. Technical Document

For frontend programmer reading, please check this [technical document](technical-document) to know how to operate those APIs.

- --
