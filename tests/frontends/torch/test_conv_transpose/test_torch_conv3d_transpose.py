# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
import torch
from hidet.testing.torch_utils import check_module
import os


@pytest.mark.parametrize(
    'in_shape,w_shape,stride,padding,output_padding',
    [[[1, 3, 224, 224, 3], [42, 3, 7, 7, 7], 4, 3, 3], [[1, 3, 224, 224, 3], [42, 3, 1, 1, 1], 2, 3, 1]],
)
@pytest.mark.parametrize('groups', [3, 1])
@pytest.mark.parametrize('dtype', [torch.float32])
def test_conv3d_transpose(in_shape, w_shape, stride, padding, output_padding, groups, dtype):
    check_module(
        model=torch.nn.ConvTranspose3d(
            in_channels=in_shape[1],
            out_channels=w_shape[0],
            kernel_size=w_shape[2:],
            stride=stride,
            padding=padding,
            output_padding=output_padding,
            groups=groups,
        ),
        args=[torch.randn(in_shape, dtype=dtype)],
    )


if __name__ == '__main__':
    pytest.main([__file__])