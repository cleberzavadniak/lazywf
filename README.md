# lazywf

The laziest web framework ever.

[![CircleCI](https://circleci.com/gh/cleberzavadniak/lazywf/tree/master.svg?style=svg)](https://circleci.com/gh/cleberzavadniak/lazywf/tree/master)

## How to use

### requirements.txt

> git+https://github.com/cleberzavadniak/lazywf.git

### server.py

In your project root, create a `server.py` script this
way:

```python
#!env python3

from lazywf import TheLaziestWebFrameworkEVER


class Lazy(TheLaziestWebFrameworkEVER):
    pass


Lazy().run()
```

(You can skip this step and simply call `python3 -m lazywf`
inside your project root directory.)


### models.yaml

Then, create a `models.yaml` in your project directory, like this:

```yaml
products:  # Your model name
    constraints:  # Some constrains you'd like to enforce
        keys: [sku]
        unique: [sku]
    validations:  # Describe some validations for your data
        sku:
            type: string
            required: true
            minlength: 16
            maxlength: 18
        name:
            type: string
            required: true
            maxlength: 64
        price:
            type: float
            required: true
        old_price:
            type: float
            required: false
            nullable: true
            default: null
```

Data validation is done using the excelent
[Cerberus](https://github.com/pyeve/cerberus)
project.

### DATABASE_URL

Export your `DATABASE_URL` environment variable:

```bash
$ export DATABASE_URL="sqlite:///database.sqlite"
```

### run

Now you can run your server:

```bash
$ python3 server.py
```

### Test with httpie

Test it using
[httpie](https://github.com/jakubroztocil/httpie):

```bash
$ http --json POST "http://localhost:8080/api/products/" sku=12345678901234567 name=TestProduct price:=19.90
$ http "http://localhost:8080/api/products/"
$ http --json PATCH "http://localhost:8080/api/products/12345678901234567" old_price:=19.90 price:=29.90
$ http "http://localhost:8080/api/products/"
$ http DELETE "http://localhost:8080/api/products/1"
$ http "http://localhost:8080/api/products/"
```


## Why I started this project

I really enjoy working with **Django**. It's a very nice
framework if you want to do some serious business without
worrying too much about little details that won't help you
at all to make your deliveries in time. It's opinionated
and I think it's good -- except when I don't want to do
anything "serious".

I think it's too difficult to get a Django project up and
running. You have to deal with your "settings.py",
configure where your templates are, enable static files
serving, write your models upfront, create migrations,
migrate, write the views, then write the templates then
run the server and finally see nothing really happening
because all you did was simply the skeleton of your
application and **now** you can start really making the
things happen as you wanted at first.

What was that, again?

I don't have the patience to deal with so much work only
to put into life something very simple I want to **play**
with.

**I am too lazy!**

## Django REST -ANYTHING- make everything even worse!

Add to all that the decision to have a REST API. Now I have
to write **serializers** or specialized views, too.

**Oh, no!**

I can't do that anymore. Really. Maybe when I was 20 years
old, but not on my age...

## Save your laziness on a DBMS

So, I decided to create a project using Bottle. But, where
should I save my data? Planning to run the app on Heroku, I
couldn't save things on the filesystem. So I found the
"dataset" project and loved it. That was **exactly** what I
needed.

## Models are still nice

I like to design models. What I don't like is to write the
models as code. Yes, you heard it. There should be a better
way.
Since "dataset" is very loose about data and I wanted some
way of validating what was coming from the REST API, I
found it suitable to validate data using "cerberus". So I
needed some place to save the validation schemata, and
decided to use **YAML** for that, since JSON is too verbose
and I am too lazy to comply with JSON strict rules (and
type all that innumerous '{' and '}' and ','...).

Also, model defining should be very simple. Your project
must have a "models.yaml" file on the root directory, from
where models definition, some constraints and validation
rules are going to be loaded.

And that is it.

## Example project using lazywf

There is an example project included on this repository.
You can copy it to use in your own project. It's as simple
as it seems. ;-)
