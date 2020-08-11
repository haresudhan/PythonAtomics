# PythonAtomics
Small wrapper files to do simple operations in python. 

## CRUD Client
Add API methods to the crud_client.py file.

## DB Wrapper and CacheWrapper
Things to replace: 
{Module} - Add the module name here.
{Model} - Add the model name from the module.


To add caching, add it in the settings.py file.

```
CACHES = {
    '{Module}' : {
        'BACKEND' : 'django.core.caches.backends.locmem.LocMemCache',
        'LOCATION' : '{Module}',
        'TIMEOUT' : None
    }
}
```