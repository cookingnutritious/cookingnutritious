#CookingNutritious
This is the backend for the cooking nutritious website. This website houses data corresponding to the cookingnutritious recipies and ingredients.

##Dependencies
This application depends on a range of different software listed below.
###python 2.7
###django 1.6
###memcached 1.4.4
###python-social-auth
    pip install python-memcached
###python-social-auth
    pip install python-social-auth
###python-openid
    pip install python-openid
###requests-oauthlib
    pip install requests-oauthlib
###djangorestframework
    pip install djangorestframework
###django rest framework extensions
    pip install drf-extensions
###drf-extensions
    pip install drf-extensions
###markdown
    pip install markdown
###django-filter
    pip install django-filter
###django-stripe-payments
    pip install django-stripe-payments==2.0b34
###django-forms-bootstrap
    pip install django-forms-bootstrap
###django-autocomplete-light
    pip install django-autocomplete-light
###django-memcached
    pip install django-memcached
###django-cors-headers
    pip install django-cors-headers

##loading USDA Database
###To import the latest SR22 data.  Simply use the `import_sr` management command
as follows:

 python ./manage.py import_sr -f data/usda/sr27asc.zip

The above assumes that the `sr27asc.zip` file is in the "data/usda/" folder.  To specify
an alternative location specify `-f <filename>`.

###To run as a background job try:

    nohup python ./manage.py import_sr -f data/usda/sr27asc.zip & > /dev/null 2>&1

###The `import_sr` command takes several options:

* --database <dbname> -- Specify an alternative database to populate.
* --food -- Create/update all foods.
* --group -- Create/Update food groups.
* --nutrient -- Create/Update nutrients.
* --weight -- Create/Update weights.
* --footnote -- Create/Update footnotes.
* --datasource -- Create/Update data sources.
* --derivation -- Create/Update data derivations.
* --source -- Create/Update sources.
* --data -- Create/Update nutrient data.'
* --all -- Create/Update all data.
