# ColonistQLearning
Analysis and Q learning method for [colonist.io](https://colonist.io/), game community found [here](https://discord.com/channels/605233308577562643/704115448769413121).

# Install
## Software Installations
Download and install [Annaconda3](https://www.anaconda.com/distribution/).

#### GPU  Software Installation
Download and install [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/).

Install Visual Studio [Build Tools 2019 and Visual C++ build tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16) (link downloads the .exe).

First determine which version of CUDA is valid for your GPU then download and install the correct version form [here](https://developer.nvidia.com/cuda-toolkit-archive).

Follow the guild on how to install cuDNN [here](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html). 

#### Environment Setup
```commandline
conda create --name QL --file conda_install
conda activate QL

pip install -r requirements.txt     
````

# Analysis
## Initial Placement
A notebook for evaluating inital placament position can be found [here](https://github.com/zactodd/ColonistQLearning/blob/master/colonist_ql/analytics/notebooks/starting_placements.ipynb). It shows a varity of metrics on what vertices are better to start on.

# Citation
Use this bibtex to cite this repository:

```
@misc{colonist_ql,
  title={Analysis and Q learning in Catan},
  author={Zachary Todd},
  year={2020},
  publisher={Github},
  journal={GitHub repository},
  howpublished={\url{https://github.com/zactodd/ColonistQLearning}},
}
```
