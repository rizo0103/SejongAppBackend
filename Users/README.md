# Django MongoDB Backend - App Template

This is a Django app starter template for the Django MongoDB Backend.
In order to use it with your version of Django: 

- Find your Django version. To do so from the command line, make sure you
  have Django installed and run:

```bash
django-admin --version
>> 5.1
```

## Create the Django app

From your shell, run the following command to create a new Django project
replacing the `{{ app_name }}` and `{{ version }}` sections. 

```bash
django-admin startapp {{ app_name }} --template https://github.com/mongodb-labs/django-mongodb-app/archive/refs/heads/{{ version }}.x.zip
```

For an app named `5_1_example_app` that runs on `django==5.1.*`
the command would look like this:

```bash
django-admin startapp 5_1_example_app --template https://github.com/mongodb-labs/django-mongodb-app/archive/refs/heads/5.1.x.zip
```
