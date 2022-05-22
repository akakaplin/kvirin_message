from dataclasses import dataclass
import yaml


@dataclass
class Feature:
    feature: str
    value: bool


@dataclass
class Pool:
    features: list[Feature]
    bridges: list[str]


def load_config(yaml_path: str) -> dict[str, Pool]:
    pools = []
    with open(yaml_path, 'r') as stream:
        config_dict = yaml.safe_load(stream.read())
        descs = config_dict['pools']
        for p in descs:
            t = Pool(**descs[p])
            pools.append(t)
    return pools
