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

package org.apache.openwhisk.core.containerpool

import org.apache.openwhisk.core.entity.MemoryLimit
import scala.collection.immutable.Map
import scala.collection.immutable.Vector
import java.time.Instant


// A Budget for every activation

class Budget(self: Run){
    var memoryIn = Map.empty[Run, Int]
    var memoryOut = Map.empty[Run, Int]
    var memoryDelta: Int = 0
    var memoryIdleTime: Long = 0.toLong
    var memoryTrajectory: String = ""
    var cpuIn = Map.empty[Run, Int]
    var cpuOut = Map.empty[Run, Int]
    var cpuDelta: Int = 0
    var cpuIdleTime: Long = 0.toLong
    var cpuTrajectory: String = ""

    var isSafeguard: Int = 0

    def setMemoryDelta(memory: Int): Unit ={
        memoryDelta = memory * MemoryLimit.MEM_UNIT
    }

    def setCpuDelta(cpu: Int): Unit = {
        cpuDelta = cpu
    }

    def addMemoryIn(list: Vector[(Run, Int, Long, Long)]): Unit = {
        list.foreach{
            case (job, value, _, _) =>
                memoryIn.updated(job, memoryIn.getOrElse(job, 0) + value)
                memoryTrajectory += (if (memoryTrajectory.isEmpty) "" else memoryTrajectory) + s"${job.msg.activationId.toString}:${value * MemoryLimit.MEM_UNIT}"
        }
    }

    def removeMemoryIn(list: Vector[Run]): Unit = {
        memoryIn --= list
    }

    def resetMemoryIn(): Unit = {
        memoryIn = Map.empty[Run, Int]
    }

    def addMemoryOut(list: Vector[(Run, Int, Long, Long)]): Unit = {
        list.foreach{
            case (job, value, _, _) =>
                memoryOut.updated(job, memoryOut.getOrElse(job, 0) + value)
                memoryTrajectory += (if (memoryTrajectory.isEmpty) "" else memoryTrajectory) + s"${job.msg.activationId}:${value * MemoryLimit.MEM_UNIT}"
        }
    }

    def removeMemoryOut(list: Vector[Run]): Unit = {
        memoryOut --= list
    }

    def resetMemoryOut(left: Option[(Int, Long, Long)]): Unit = {
        memoryOut = Map.empty[Run, Int]

        // Update rest of idle time in harvested resource pool
        left match {
            case Some((value, start, end)) => memoryIdleTime = memoryIdleTime + (Instant.now.toEpochMilli - start) * (value * MemoryLimit.MEM_UNIT)
            case None =>
        }
    }

    def addCpuIn(list: Vector[(Run, Int, Long, Long)]): Unit = {
        list.foreach {
            case (job, value, _, _) =>
                cpuIn = cpuIn.updated(job, cpuIn.getOrElse(job, 0) + value)
                cpuTrajectory += (if (cpuTrajectory.isEmpty) "" else cpuTrajectory) + s"${job.msg.activationId}:$value"
        }
    }

    def removeCpuIn(list: Vector[Run]): Unit = {
        cpuIn --= list
    }

    def resetCpuIn(): Unit = {
        cpuIn = Map.empty[Run, Int]
    }

    def addCpuOut(list: Vector[(Run, Int, Long, Long)]): Unit = {
        list.foreach{
            case (job, value, start, _) =>
                cpuOut.updated(job, cpuOut.getOrElse(job, 0) + value)
                cpuIdleTime = cpuIdleTime + (Instant.now.toEpochMilli - start) * value
                cpuTrajectory += (if (cpuTrajectory.isEmpty) "" else cpuTrajectory) + s"${job.msg.activationId.toString}:-${value}"
        }
    }

    def removeCputOut(list: Vector[Run]): Unit = {
    }

    def resetCpuOut(left: Option[(Int, Long, Long)]): Unit = {
    }

    def totalIdleTime: (String, String) = {((memoryIdleTime).toString, (cpuIdleTime).toString)}

    def summary(): (String, String) = {
        val id = self.msg.activationId.toString
        val (memoryIdle, cpuIdle) = totalIdleTime
        val trajectory: String = s"${isSafeguard};${memoryDelta} ${cpuDelta};${memoryIdle} ${cpuIdle};${memoryTrajectory};${cpuTrajectory}"
        (id, trajectory)
    }
}


//// TODO What does the left match {} do in resetMemoryOut ...
