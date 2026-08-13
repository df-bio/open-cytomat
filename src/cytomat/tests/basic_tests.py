import sys

sys.path.insert(1, "C:/labhub/Repos/smartlab-network/open-cytomat/src")

from cytomat.config import load_config

config = load_config()

print(config.com_port)
