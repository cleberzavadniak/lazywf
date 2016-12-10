#lazywf

The laziest web framework ever.

[![CircleCI](https://circleci.com/gh/cleberzavadniak/lazywf/tree/master.svg?style=svg)](https://circleci.com/gh/cleberzavadniak/lazywf/tree/master)

## Why I started this project

I really enjoy working with **Django**. It's a very nice
framework if you want to do some serious business without
worrying too much about little details that won't help you
at all to make your deliveries in time. It's opinionated
and I think it's good. Except when I don't want to do
anything "serious".

Really, it's too difficult to get a Django project up and
running. You have to deal with your "settings.py",
configure where your templates are, enable static files
serving, write your models upfront, create migrations,
migrate, write the views, then write the templates then
run the server and finally see nothing really happening
because all you did was simply the skeleton of your
application and **now** you can start really making the
things happen as you wanted at first.

What was that, again?

Man, I don't have the patience to deal with so much only
to put into life something very simple I want to play with.

**I am too lazy!**

## Django REST -ANYTHING- make everything even worse!

Add to all that the decision to have a REST API. Now I have
to write serializers or specialized views, too.

**Oh, no, God!, no!**

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
