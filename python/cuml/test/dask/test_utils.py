# Copyright (c) 2019, NVIDIA CORPORATION.
#
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
#

import cupy as cp

from cuml.dask.common.utils import register_serialization

from cuml.naive_bayes.naive_bayes import MultinomialNB

from distributed.protocol.serialize import serialize


def test_regsiter_serialization():

    """
    Assuming here that the Dask serializers are well-tested.
    This test-case is only validating that register_serialization
    actually provides the expected serializers on the expected
    objects.
    """

    mnb = MultinomialNB()

    X = cp.sparse.random(1, 5)
    y = cp.array([0])

    mnb.fit(X, y)

    stype, sbytes = serialize(mnb)

    assert stype['serializer'] == 'pickle'

    register_serialization()

    stype, sbytes = serialize(mnb, serializers=['cuda'])

    assert stype['serializer'] == 'cuda'

    stype, sbytes = serialize(mnb, serializers=['dask'])

    assert stype['serializer'] == 'dask'
