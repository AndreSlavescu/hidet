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
from typing import Any, Sequence
from hidet.ir.type import DataType
from .floats import float32, float16, bfloat16
from .integer import int8, uint8
from .integer_subbyte import int4b, uint4b
from .boolean import boolean


class VectorType(DataType):
    def __init__(self, lane_type: DataType, num_lanes: int):
        name = '{}x{}'.format(lane_type.name, num_lanes)
        short_name = '{}x{}'.format(lane_type.short_name, num_lanes)
        nbytes = (
            lane_type.nbytes * num_lanes if not lane_type.is_integer_subbyte() else lane_type.nbits * num_lanes // 8
        )
        super().__init__(name, short_name, nbytes)
        self._num_lanes: int = num_lanes
        self._lane_type: DataType = lane_type

        if lane_type.is_vector():
            raise ValueError('Cannot create a vector type of vectors')

    def is_float(self) -> bool:
        return False

    def is_integer(self) -> bool:
        return False

    def is_vector(self) -> bool:
        return True

    def is_complex(self) -> bool:
        return False

    @property
    def num_lanes(self) -> int:
        return self._num_lanes

    @property
    def lane_type(self) -> DataType:
        return self._lane_type

    def constant(self, value: Sequence[Any]):
        from hidet.ir.expr import constant

        value = [self.lane_type.constant(v) for v in value]
        if len(value) != self.num_lanes:
            raise ValueError('Invalid vector constant, expect {} elements, got {}'.format(self.num_lanes, len(value)))
        return constant(value, self)

    @property
    def one(self):
        return self.constant([self.lane_type.one] * self.num_lanes)

    @property
    def zero(self):
        return self.constant([self.lane_type.zero] * self.num_lanes)

    @property
    def min_value(self):
        return self.constant([self.lane_type.min_value] * self.num_lanes)

    @property
    def max_value(self):
        return self.constant([self.lane_type.max_value] * self.num_lanes)


int8x4 = VectorType(int8, 4)
i8x4 = int8x4

uint8x4 = VectorType(uint8, 4)
u8x4 = uint8x4

float32x1 = VectorType(float32, 1)
f32x1 = float32x1

float32x2 = VectorType(float32, 2)
f32x2 = float32x2

float32x4 = VectorType(float32, 4)
f32x4 = float32x4

float32x8 = VectorType(float32, 8)
f32x8 = float32x8

float16x1 = VectorType(float16, 1)
f16x1 = float16x1

float16x2 = VectorType(float16, 2)
f16x2 = float16x2

float16x4 = VectorType(float16, 4)
f16x4 = float16x4

float16x8 = VectorType(float16, 8)
f16x8 = float16x8

int4bx2 = VectorType(int4b, 2)
i4x2 = int4bx2

uint4bx2 = VectorType(uint4b, 2)
u4x2 = uint4bx2

int4bx8 = VectorType(int4b, 8)
i4x8 = int4bx8

uint4bx8 = VectorType(uint4b, 8)
u4x8 = uint4bx8

bfloat16x2 = VectorType(bfloat16, 2)


def vectorize(base_dtype: DataType, num_lanes: int) -> VectorType:
    table = {
        (float32, 1): float32x1,
        (float32, 2): float32x2,
        (float32, 4): float32x4,
        (float32, 8): float32x8,
        (float16, 1): float16x1,
        (float16, 2): float16x2,
        (float16, 4): float16x4,
        (float16, 8): float16x8,
        (int8, 4): int8x4,
        (uint8, 4): uint8x4,
        (boolean, 4): int8x4,
        (bfloat16, 2): bfloat16x2,
    }
    if (base_dtype, num_lanes) in table:
        return table[(base_dtype, num_lanes)]
    else:
        raise ValueError('Cannot vectorize {}x{}'.format(base_dtype, num_lanes))
