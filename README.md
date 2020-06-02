# ColonistQLearning
Analysis and Q learning method for colonist.io
# Install
## Software Installations
Download and install [Annaconda3](https://www.anaconda.com/distribution/).

#### GPU Usage Software Installation
Download and install [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/).

Install Visual Studio [Build Tools 2019 and Visual C++ build tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16) (link downloads the .exe).

First determine which version of CUDA a valid for your GPU then download and install the correct version form [here](https://developer.nvidia.com/cuda-toolkit-archive).

Follow the guild on how to install cuDNN [here](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html). 

#### Environment Setup
```commandline
conda create --name QL --file conda_install
conda activate QL

pip install -r requirements.txt     
````



