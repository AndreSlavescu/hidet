# Hidet: An Open-Source Deep Learning Compiler
[**Documentation**](http://hidet.org/docs)  |
[**Research Paper**](https://dl.acm.org/doi/10.1145/3575693.3575702)  |
[**Releases**](https://github.com/hidet-org/hidet/releases) |
[**Contributing**](https://hidet.org/docs/stable/developer-guides/contributing.html)

![GitHub](https://img.shields.io/github/license/hidet-org/hidet)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/hidet-org/hidet/tests.yaml)


Hidet is an open-source deep learning compiler, written in Python. 
It supports end-to-end compilation of DNN models from PyTorch and ONNX to efficient cuda kernels.
A series of graph-level and operator-level optimizations are applied to optimize the performance.

Currently, hidet focuses on optimizing the inference workloads on NVIDIA GPUs, and requires
- Linux OS
- CUDA Toolkit 11.6+
- Python 3.9+

## Getting Started

### Installation
Please install hidet via
```bash
pip install hidet
```

You can also install hidet via [building from source](https://docs.hidet.org/stable/getting-started/build-from-source.html#).

### Usage

Optimize a PyTorch model through hidet (require PyTorch 2.3):
```python
import torch

# Define pytorch model
model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True).cuda().eval()
x = torch.rand(1, 3, 224, 224).cuda()

# Compile the model through Hidet
# Optional: set optimization options (see our documentation for more details)
#   import hidet 
#   hidet.torch.dynamo_config.search_space(2)  # tune each tunable operator
model_opt = torch.compile(model, backend='hidet')  

# Run the optimized model
y = model_opt(x)
```
See the following tutorials to learn other usages:
- [Quick Start](http://hidet.org/docs/stable/gallery/getting-started/quick-start.html)

## Publication
Hidet originates from the following research work:

>  **Hidet: Task-Mapping Programming Paradigm for Deep Learning Tensor Programs**  
>  Yaoyao Ding, Cody Hao Yu, Bojian Zheng, Yizhi Liu, Yida Wang, and Gennady Pekhimenko.  
>  ASPLOS '23

If you used **Hidet** in your research, welcome to cite our
[paper](https://dl.acm.org/doi/10.1145/3575693.3575702).

## Development 
Hidet is currently under active development by a team at [CentML Inc](https://centml.ai/). 

## Contributing
We welcome contributions from the community. Please see 
[contribution guide](https://hidet.org/docs/stable/developer-guides/contributing.html)
for more details.

## License
Hidet is released under the [Apache 2.0 license](LICENSE).
