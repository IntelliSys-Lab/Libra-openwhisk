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
        const numberOfStrings = 200000; // Adjusted for memory usage
        const stringLength = 256; // Length of each random string in bytes before hex conversion

        let largeArray = [];

        for (let i = 0; i < numberOfStrings; i++) {
            // Generate a random string and add it to the array
            const randomString = crypto.randomBytes(stringLength).toString('hex');
            largeArray.push(randomString);
        }

        // CPU-intensive task: Sort the array
        largeArray.sort();

        // CPU-intensive task: Find prime numbers (additional CPU load)
        const primes = findPrimes(10000); // Find prime numbers up to 10000

        return { arrayLength: largeArray.length, primesCount: primes.length };
    };

    const findPrimes = (max) => {
        const sieve = [];
        const primes = [];
        for (let i = 2; i <= max; ++i) {
            if (!sieve[i]) {
                // i has not been marked -- it is prime
                primes.push(i);
                for (let j = i << 1; j <= max; j += i) {
                    sieve[j] = true;
                }
            }
        }
        return primes;
    };

    try {
        const result = memoryIntensiveTask();
        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Memory and CPU-intensive task completed', result }),
        };
    } catch (error) {
        console.error('Error during memory and CPU-intensive task:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error during memory and CPU-intensive task', error: error.message }),
        };
    }
};

