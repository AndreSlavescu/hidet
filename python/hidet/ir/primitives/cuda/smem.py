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
from typing import Union

from hidet.ir.expr import Expr, Call
from hidet.ir.expr import Var
from hidet.ir.stmt import BlackBoxStmt, Stmt
from hidet.ir.type import DataType, PointerType, data_type
from hidet.ir.func import Function
from hidet.ir.primitives.func import register_primitive_function, call_primitive_func
from hidet.utils import initialize


@initialize()
def register_functions():
    from hidet.lang import script, attrs, cast

    for dtype in [
        'int8',
        'uint8',
        'uint32',
        'uint64',
        'int32',
        'float16',
        'float32',
        'tfloat32',
        'bfloat16',
        'float8_e4m3',
        'float8_e5m2',
        'bool',
        'int4b',
        'uint4b',
        'int2b',
        'uint2b',
        'int1b',
        'uint1b',
    ]:
        func_name = f'cuda_dynamic_shared_memory_{dtype}'
        dtype = data_type(dtype)

        @script
        def cuda_dynamic_shared_memory(byte_offset: int) -> ~dtype:
            attrs.func_kind = 'cuda_internal'
            attrs.func_name = func_name
            dynamic_smem = PointerType(
                base_type='uint8', specifiers=['extern', '__align__(128)', '__shared__'], use_bracket=True
            )
            return cast(~dynamic_smem[byte_offset], ~dtype)

        assert isinstance(cuda_dynamic_shared_memory, Function)
        register_primitive_function(cuda_dynamic_shared_memory.name, cuda_dynamic_shared_memory)


def dynamic_shared_memory(byte_offset: Union[Expr, int], dtype: Union[DataType, str]) -> Call:
    dtype: DataType = data_type(dtype)
    func_name = f'cuda_dynamic_shared_memory_{dtype.name}'
    return call_primitive_func(func_name, [byte_offset])


def set_kernel_max_dynamic_smem_bytes(func: Var, max_dynamic_smem_bytes: Union[Expr, int]) -> Stmt:
    from hidet.ir.expr import convert

    max_dynamic_smem_bytes = convert(max_dynamic_smem_bytes)
    template_string = r'cudaFuncSetAttribute({}, cudaFuncAttributeMaxDynamicSharedMemorySize, {});'
    return BlackBoxStmt(template_string, func, max_dynamic_smem_bytes)
