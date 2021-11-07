from azureml.core import Workspace

try:
    ws = Workspace.from_config()
    print(ws)
except:
    print('Workspace not found')
