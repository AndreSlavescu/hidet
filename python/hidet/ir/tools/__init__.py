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
from .type_infer import infer_type, TypeInfer
from .util_functors import collect
from .rewriter import rewrite, MapBasedRewriter
from .free_var_collector import collect_free_vars
from .printer import IRPrinter, astext
from .simplifier import simplify, simplify_to_int
from .hasher import ExprHash
from .renamer import rename_funcs

# from .ir_dumper import astext2, parse
