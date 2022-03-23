# storyly-api

Case Study

## Run

```bash
https://github.com/ertongcan/storyly_case_study.git
cd storyly_case_study
COPY .env.sample AS .env
```

### Setup

```bash
python3 -m venv venv
source venv/bin/activate OR \venv\Scripts\activate
pip install -r requirements.txt
```

### DB Setup

Follow these steps run models migration, at the end of below commands, models in the app will be created on specified db(from .env file)

```bash
set FLASK_APP=api/__init__.py
flask db init
flask db migrate
flask db upgrade
```

Then

```bash
flask run
```

### Run Tests
```bash
python tests.py
```

## Endpoints

`GET '/stories/<string:token>'` - get stories by given app token <br/>
`GET '/stories_enhanced/<string:token>'` - get stories by app token (peformance optimized version) <br/>
`POST '/event/<string:token>'` - save user events <br/>
`GET '/event/dau/<string:token>/<string:event_date>'` - get daily active users

## Load Test

Tests are taken place using apache ab testing tool by following command;
```bash
ab -k -n 100 -c 10 <URL_TO_TEST>
```

### Test Results

### Without optimization <br/><br/><br/>
![alt text](https://github.com/ertongcan/storyly_case_study/blob/main/ab_wo_cache.PNG)

### Optimized <br/><br/><br/>
![alt text](https://github.com/ertongcan/storyly_case_study/blob/main/ab_cached.PNG)

