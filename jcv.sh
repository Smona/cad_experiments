#!/usr/bin/env sh

export CAD_WIDTH=1200
export CAD_HEIGHT=1080
export THEME=dark
# Overlay controls on top of 3D view
export GLASS_MODE=1

# echo [JCV] Creating a Jupyter kernel specification called 'jcv' for this conda environment
# python -m ipykernel install --name jcv --display-name jcv

JCV_PATH=~/.jcv
VIEWER_PATH=$(python -c "import os, jupyter_cadquery.viewer.server as c; print(os.path.dirname(c.__file__))")

echo [JCV] Copying the voila notebook to $JCV_PATH
mkdir -p $JCV_PATH
cp $VIEWER_PATH/viewer.ipynb $JCV_PATH/

echo [JCV] Signing the voila notebook
jupyter trust $JCV_PATH/viewer.ipynb

echo [JCV] Starting Jupyter CadQuery Viewer
voila --theme=$THEME \
    --enable_nbextensions=1 \
    --show_tracebacks=1 \
    --VoilaExecutor.kernel_name=jcv \
    --VoilaConfiguration.file_whitelist="favicon.ico" \
    --VoilaConfiguration.file_whitelist=".*\.js" \
    $JCV_PATH/viewer.ipynb
