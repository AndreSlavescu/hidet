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
import os
import sys
import subprocess


@pytest.mark.requires_cuda
def test_lazy_initialization():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    python_path = sys.executable
    cmd = [python_path, os.path.join(cur_dir, 'lazy_init_sample.py')]
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    pytest.main([__file__])
