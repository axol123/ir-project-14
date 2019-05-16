/*
 * Licensed to Elasticsearch under one or more contributor
 * license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright
 * ownership. Elasticsearch licenses this file to you under
 * the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.elasticsearch.client.ml;

import org.elasticsearch.common.xcontent.XContentParser;
import org.elasticsearch.client.AbstractHlrcStreamableXContentTestCase;
import org.elasticsearch.xpack.core.ml.action.MlInfoAction.Response;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Predicate;

public class MlInfoActionResponseTests extends
    AbstractHlrcStreamableXContentTestCase<Response, MlInfoResponse> {

    @Override
    public MlInfoResponse doHlrcParseInstance(XContentParser parser) throws IOException {
        return MlInfoResponse.fromXContent(parser);
    }

    @Override
    public Response convertHlrcToInternal(MlInfoResponse instance) {
        return new Response(instance.getInfo());
    }

    @Override
    protected Predicate<String> getRandomFieldsExcludeFilter() {
        return p -> true;
    }

    @Override
    protected Response createTestInstance() {
        int size = randomInt(10);
        Map<String, Object> info = new HashMap<>();
        for (int j = 0; j < size; j++) {
            info.put(randomAlphaOfLength(20), randomAlphaOfLength(20));
        }
        return new Response(info);
    }

    @Override
    protected Response createBlankInstance() {
        return new Response();
    }
}
