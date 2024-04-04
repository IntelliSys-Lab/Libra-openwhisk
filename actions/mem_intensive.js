/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const memoryIntensiveFunction = async () => {
  // Allocate a buffer of 3GB
  const buffer = Buffer.alloc(3 * 1024 * 1024 * 1024);

  // Perform some operations to ensure the memory is used (not optimized away)
  for (let i = 0; i < buffer.length; i += 1024 * 1024) {
    buffer[i] = 1;
  }

  console.log('Memory-intensive operation completed.');

  // Return a response or perform further operations
  return {
    status: 'completed',
    memoryUsage: process.memoryUsage().heapUsed / 1024 / 1024 + ' MB'
  };
};

// Export the function as 'main' to conform with the serverless platform's expectations
module.exports = { main: memoryIntensiveFunction };

