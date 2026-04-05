# Dropout Prediction pipeline
> Made by ubiquiste for MLOps' laboratory assignments #3 and #4.

## Model description

This pipeline is aimed at training a series of moderately complex machine learning algorithms applied to a classic [Student Dropout](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success) dataset from UCI repo.
The model itself solves a binary classification task of predicting whether a particular student has a high probability of leaving university before getting a degree (`class 1`) or not (`class 0`).

## Local deployment
> [!IMPORTANT]
> Instructions below will work **if and only if** you have `uv` project manager and `git` SCM installed in your system.

```bash
git clone https://github.com/antidude-z/dropout_prediction.git
cd ./dropout_prediction
uv sync
```

### Usage

A brief overview of commands pre-defined for developer's convenience:
#### Training
```bash
uv run train-model
```
Run the training process and save artifacts inside `/mlflow` folder.
This command also performs data obtainment and preprocessing. When those steps are done, 4 different models are trained by default: `LogisticRegression`, `RandomForestClassifier`, `XGBClassifier` and `CatBoostClassifier`.
Each of these models is in turn fitted with various parameters listed in `/src/config.py`, and best model (algorithm- and parameter-wise) is chosen based on the value of ROC-AUC metric.

> [!TIP]
> The whole process tends to be quite slow (reaching ~20 mins on my PC), so setting `LIGHTWEIGHT=true` environment variable is advised in case you want quick results without achieving maximum model quality. This parameter excludes `XGBClassifier` and `CatBoostClassifier` models from training, drastically reducing execution time.
#### Deployment
```bash
uv run serve-model
```
Serve the best-performing model using MLflow inference engine (`mlflow models serve...`) on *port 8080*. 
#### Health check
```bash
uv run health-check
```
This is a simple utility which carries out an accuracy metric test on 50 random entries from the test split. Allows to check if the service is running and properly functioning.
#### Running MLFlow UI
```bash
uv run serve-ui
```
Serves a web interface on *port 5000* where you can evaluate all the data recorded during last training run by yourself.

## Jenkins deployment
> [!IMPORTANT]
> Instructions below will work **if and only if** you have `git`, `Jenkins` and `docker` installed in your system.

1. Create a new `Pipeline`. 
2. Set script definition to *Pipeline script from SCM*.
3. Set SCM to `Git`.
4. Type "https://github.com/antidude-z/dropout_prediction.git" in *Repository URL* field.
5. Click *Save*.
6. Run the newly created pipeline as usual. The first run will be aborted in order for Jenkins to fetch `LIGHTWEIGHT` parameter field inside the UI.
7. Run the pipeline again - this time everything should work normally.

On a successful run, all of the operations described in [Usage](#usage) will be performed automatically using containerization. As a result, two docker containers should now be running in the background: `ml_model` on port 8080, which serves inference for your model, and `mlflow_ui` on port 5000. Those will be recreated on each pipeline run.
