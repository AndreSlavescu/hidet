import pytest

import hidet
from hidet.ir.task import Task
from hidet.ir import primitives
from hidet.ir.dtypes import float32
from hidet.runtime import CompiledGraph
from hidet.graph.ops.utils import input_like, Operator, Tensor, compute, TensorInput
import torch


class InplaceReLUTask(Task):
    def __init__(self, x: TensorInput):
        y = compute(name='y', shape=x.shape, fcompute=lambda *indices: primitives.max(x[indices], x.type.dtype.zero))
        super().__init__(name='inplace_relu', inputs=[x], outputs=[y], share_map={0: 0})  # share y with x


class InplaceReLUOp(Operator):
    def __init__(self, x: Tensor):
        super().__init__(inputs=[x], attributes={}, task=InplaceReLUTask(input_like(x, 'x')))


def inplace_relu(x: Tensor) -> Tensor:
    return InplaceReLUOp(x).outputs[0]


def test_inplace_relu(device):
    x = hidet.symbol([1, 10], dtype=float32, device=device)
    y = inplace_relu(x)
    graph = hidet.trace_from(y)
    xx = hidet.randn_like(x)

    y1 = graph(xx)
    assert y1.storage is xx.storage

    compiled_graph: CompiledGraph = graph.build()

    compiled_graph.clear_dispatch_table()
    y2 = compiled_graph(xx)  # run in slow path
    assert y2.storage is xx.storage

    y3 = compiled_graph(xx)  # run in fast path
    assert y3.storage is xx.storage

    # y1, y2, y3 should be equal
    yy = hidet.ops.relu(xx)
    hidet.utils.assert_close(y1, yy)


@pytest.mark.requires_cuda
@pytest.mark.parametrize(
    "input_shape,index_shape,src_shape,dim",
    [[(22, 33), (11, 11), (11, 11), 0], [(257, 256), (128, 128), (128, 128), 1]],
)
def test_inplace_scatter_add(input_shape, index_shape, src_shape, dim):
    input_tensor = torch.randint(0, 3, input_shape).to(dtype=torch.float32).cuda()

    index_tensor = torch.randint(0, input_shape[dim], index_shape).cuda()

    src = torch.randint(0, 10, src_shape).to(dtype=torch.float32).cuda()

    input_hidet = hidet.from_torch(input_tensor.clone())
    index_hidet = hidet.from_torch(index_tensor.clone())
    src_hidet = hidet.from_torch(src.clone())

    output_torch = input_tensor.scatter_add_(dim, index_tensor, src)
    output_hidet = hidet.ops.scatter_add_(input_hidet, dim, index_hidet, src_hidet)

    hidet.utils.assert_close(output_hidet, output_torch)
    hidet.utils.assert_close(input_hidet, input_tensor)


@pytest.mark.requires_cuda
def test_inplace_scatter():
    src = torch.arange(1, 7).reshape((2, 3)).to(dtype=torch.float16).cuda()
    index = torch.tensor([[0, 1, 2], [2, 1, 0]]).to(dtype=torch.int64).cuda()
    input = torch.zeros(3, 5, dtype=src.dtype).to(dtype=torch.float16).cuda()

    hidet_src = hidet.from_torch(src.clone())
    hidet_index = hidet.from_torch(index.clone())
    hidet_input = hidet.from_torch(input.clone())

    output_torch = input.scatter_(0, index, src)
    output_hidet = hidet.ops.scatter_(hidet_input, 0, hidet_index, hidet_src, reduce='replace')

    hidet.utils.assert_close(output_hidet, output_torch)
    hidet.utils.assert_close(hidet_input, input)

    output_torch_add = input.scatter_(0, index, src, reduce='add')
    output_hidet_add = hidet.ops.scatter_(hidet_input, 0, hidet_index, hidet_src, reduce='add')

    hidet.utils.assert_close(output_hidet_add, output_torch_add)
    hidet.utils.assert_close(hidet_input, input)


if __name__ == '__main__':
    pytest.main([__file__])
