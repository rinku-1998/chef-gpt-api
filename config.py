import yaml


class Config():

    # 1. 資料庫
    DB_URL = 'postgresql://chef:chef@127.0.0.1:5432/chefgpt'

    # 2. 語料
    DOC_DIR = 'data/recipe/'

    # 3. Embedding
    EMB_DEVICE = 'cpu'
    EMB_MODEL_NAME = 'shibing624/text2vec-base-chinese'

    # 3. Qdrant
    QDRANT_URL = 'http://localhost:6333'
    COLLECTION_NAME = 'recipe'

    # 4. LLM
    LLM_MODEL_PATH = 'weight/chinese-alpaca-2-7b.Q5_0.gguf'
    TEMPERATURE = 0.2

    def __init__(self, config_path=r'env.yml') -> None:

        # 1. 讀取 yaml 檔
        config_yml = None
        with open(config_path, 'r', encoding='utf-8') as f:
            config_yml = yaml.safe_load(f)

        # 2. 更新資料
        for key, value in config_yml.items():
            setattr(self, key, value)
