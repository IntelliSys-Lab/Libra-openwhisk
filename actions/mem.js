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

const crypto = require('crypto');

exports.main = async (event) => {
    const memoryIntensiveTask = () => {
        // Adjust the number of strings and/or the length of each string to fit within 512 MB
        const numberOfStrings = 250000; // Reduced number of strings
        const stringLength = 256; // Reduced length of each string to 256 bytes (before hex conversion)

        let largeArray = [];

        for (let i = 0; i < numberOfStrings; i++) {
            // Generate a random string and add it to the array
            const randomString = crypto.randomBytes(stringLength).toString('hex');
            largeArray.push(randomString);
        }

        // Perform some operations on the large array (e.g., sort, filter, reduce)
        largeArray = largeArray.sort();

        // Optionally clear the array to free memory if needed
        // largeArray = [];

        return largeArray.length; // Return the length or any other relevant information
    };

    try {
        const result = memoryIntensiveTask();
        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Memory-intensive task completed', length: result }),
        };
    } catch (error) {
        console.error('Error during memory-intensive task:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error during memory-intensive task', error: error.message }),
        };
    }
};

