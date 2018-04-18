import yaml


def file_lines(p_path):
    with open(p_path, 'r') as file:
        return file.read().splitlines()


def dict_from_yaml(p_path):
    with open(p_path, 'r') as file:
        return yaml.safe_load(file)


def write_dict(p_path, p_data_map):
    with open(p_path, 'w') as file:
        file.write(yaml.dump(p_data_map, default_flow_style=False, allow_unicode=True))
