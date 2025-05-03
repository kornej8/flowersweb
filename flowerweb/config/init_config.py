import os
import yaml
import os

class SecretFounderException(Exception):
    ...


class ConfigWithSecrets:
    secret_keyword = 'flower_secret'
    secret_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'secrets')
    def __init__(self, config):
        self.config = config

    def _read_secret(self, secret_code):
        secret_file = secret_code.lstrip(self.secret_keyword).replace(':', '.')
        try:
            with open(f'{self.secret_folder}/{secret_file}') as f:
                return f.readline().strip()
        except FileNotFoundError as e:
            raise SecretFounderException(f"Didnt find {secret_code} in secrets/{secret_file}")

    def decode_secret(self, secret_code):
        if str(secret_code).startswith(self.secret_keyword):
            return self._read_secret(secret_code)
        return secret_code

    def get(self, key, default_value=None):
        value = self.config.get(key, default_value)
        if isinstance(value, str | int):
            return self.decode_secret(value)
        return ConfigWithSecrets(self.config.get(key, default_value))


class Config:
    def __init__(self, cfg='cfg.yaml'):
        self.cfg_path = os.path.join(os.path.dirname(__file__), cfg)

    def get(self):
        with open(self.cfg_path, 'r') as cfg:
            cfg = ConfigWithSecrets(yaml.safe_load(cfg))
        return cfg
