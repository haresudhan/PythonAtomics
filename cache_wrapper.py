from crud_client import CRUDAPI
from django.core.cache import caches

CACHE_KEY = "{Module}Cache"

class CacheWrapper(CRUDAPI):

    def create_model(self, key: str, value):
        super().create_model(key,value)
        caches[CACHE_KEY].set(key,value)

    def retrieve_model(self, key: str):
        if self.does_key_already_exists(key):
            return caches[CACHE_KEY].get(key)
        else:
            value = super().retrieve_model(key)
            caches[CACHE_KEY].set(key,value)
            return value

    def delete_model(self, key:str):
        super().delete_model(key)
        caches[CACHE_KEY].delete(key)

    def update_model(self, key: str, value):
        super().update_model(key,value)
        caches[CACHE_KEY].set(key,value)

    def get_all_models(self):
        # TODO: 
        pass

    def delete_all_models(self):
        caches[CACHE_KEY].clear()

    def does_key_already_exists(self, key):
        return caches[CACHE_KEY].get(key)