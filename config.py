import yaml


class Config():

    DB_URL = 'postgresql://chef:chef@127.0.0.1:5432/chefgpt'

    def __init__(self, config_path=r'env.yml') -> None:

        # 1. 讀取 yaml 檔
        config_yml = None
        with open(config_path, 'r', encoding='utf-8') as f:
            config_yml = yaml.safe_load(f)

        # 2. 更新資料
        for key, value in config_yml.items():
            setattr(self, key, value)
