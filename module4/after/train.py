
import joblib

from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
import sklearn


dataset_x, dataset_y = load_diabetes(return_X_y=True)

model = Ridge().fit(dataset_x, dataset_y)

joblib.dump(model, 'sklearn_regression_model.pkl')

print('Model trained')


import numpy as np

from azureml.core import Dataset


np.savetxt('features.csv', dataset_x, delimiter=',')
np.savetxt('labels.csv', dataset_y, delimiter=',')
from azureml.core.run import Run
run = Run.get_context()
ws = run.experiment.workspace
datastore = ws.get_default_datastore()
datastore.upload_files(files=['./features.csv', './labels.csv'],
                       target_path='sklearn_regression/',
                       overwrite=True)

input_dataset = Dataset.Tabular.from_delimited_files(path=[(datastore, 'sklearn_regression/features.csv')])
output_dataset = Dataset.Tabular.from_delimited_files(path=[(datastore, 'sklearn_regression/labels.csv')])

import sklearn

from azureml.core import Model
from azureml.core.resource_configuration import ResourceConfiguration

model = Model.register(workspace=ws,
                       model_name='my-sklearn-model-docker',                # Name of the registered model in your workspace.
                       model_path='./sklearn_regression_model.pkl',  # Local file to upload and register as a model.
                       model_framework=Model.Framework.SCIKITLEARN,  # Framework used to create the model.
                       model_framework_version=sklearn.__version__,  # Version of scikit-learn used to create the model.
                       sample_input_dataset=input_dataset,
                       sample_output_dataset=output_dataset,
                       resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=0.5),
                       description='Ridge regression model to predict diabetes progression.',
                       tags={'area': 'diabetes', 'type': 'regression'})

print('Name:', model.name)
print('Version:', model.version)
