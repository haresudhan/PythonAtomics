import os
from cryptography.fernet import Fernet

from crud_client import CRUDAPI
from {module}.models import {Model}

class DBWrapper(CRUDAPI):
    def __init__(self):
        super().__init__()
        self.fernet = Fernet(self._get_encryption_key())

    def create_model(self, key: str, value):
        super().create_model(key,value)
        {Model}(key=key, value=value).save()
        # {Model}(key=key, value=self._encrypt_value(value)).save()

    def retrieve_model(self, key: str):
        if self.does_key_already_exists(key):
            model = {Model}.objects.get(key)
            return model.value
            # return self._decrypt_value(model.value)
        else:
            value = super().retrieve_model(key)
            model = {Model}(key=key, value=value)
            # model = {Model}(key=key, value=self._encrypt_value(value))
            model.save()
            return model

    def delete_model(self, key:str):
        super().delete_model(key)
        {Model}.objects.get(key).delete()

    def update_model(self, key: str, value):
        super().update_model(key,value)
        model = {Model}.objects.get(key)
        model.value = value
        # model.value = self._encrypt_value(value)

    def get_all_models(self):
        return {Model}.objects.all()

    def delete_all_models(self):
        return self.get_all_models().delete()

    def does_key_already_exists(self, key):
        return {Model}.objects.filter(key).exists()


    # MARK: Encryption Methods
    def _get_encryption_key(self):
        try:
            return os.environ["ENCRYPTION_KEY"]
        except:
            self._generate_encryption_key()
            return os.environ['ENCRYPTION_KEY']

    def _generate_encryption_key(self):
        encryption_key = Fernet.generate_key().decode()
        os.environ['ENCRYPTION_KEY'] = encryption_key

    def _encrypt_value(self, value):
        return self.fernet.encrypt(value.encode()).decode()

    def _decrypt_value(self, secret):
        return self.fernet.decrypt(secret.encode()).decode()