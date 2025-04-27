import os
import yaml


class Config:
    def __init__(self, cfg='cfg.yaml'):
        self.cfg_path = os.path.join(os.path.dirname(__file__), cfg)

    def get(self):
        with open(self.cfg_path, 'r') as cfg:
            cfg = yaml.safe_load(cfg)
        return cfg


