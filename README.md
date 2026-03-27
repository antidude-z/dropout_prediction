# Dropout Prediction pipeline
Made by ubiquiste for MLOps' laboratory assignments #3 and #4.

## Local deployment

```bash
git clone ...
cd ./dropout_prediction
uv sync
```

### Usage

```bash
uv run train-model
uv run serve-model
uv run health-check
uv run serve-ui
```

## Jenkins deployment

1. Create a new `Pipeline`
2. Set definition to "Pipeline script from SCM"
3. Set SCM to "Git"
4. Type "..." in Repository URL field
5. Click "Save"
6. Run the newly created pipeline as usual
