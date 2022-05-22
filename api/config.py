from dataclasses import dataclass
from typing import Dict, List
import yaml


@dataclass
class Feature:
    feature: str
    value: bool


@dataclass
class Pool:
    features: List[Feature]
    bridges: List[str]


def load_config(yaml_path: str) -> Dict[str, Pool]:
    pools = {}
    with open(yaml_path, 'r') as stream:
        config_dict = yaml.safe_load(stream.read())
        descs = config_dict['pools']
        for p in descs:
            t = Pool(**descs[p])
            pools[p] = t
    return pools
