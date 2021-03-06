# major refactor 2: control logic change, move the looping logic outside of the solver nodes
# 21-Jun-2017 DZ
# Assigner node is an action node that put one variable onto blackboard
# Other solver nodes will read the assigned unknown variable from the board
# and try to solve it

# Copyright 2017 University of Washington

# Developed by Dianmu Zhang and Blake Hannaford
# BioRobotics Lab, University of Washington

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sympy as sp
import numpy as np
from sys import exit

from ikbtfunctions.helperfunctions import *
from ikbtbasics.kin_cl import *
# special classes for Inverse kinematics in sympy
from ikbtbasics.ik_classes import *

import b3 as b3          # behavior trees


class assigner(b3.Action):
    def tick(self, tick):
        unknowns = tick.blackboard.get("unknowns")

        counter = tick.blackboard.get("counter")
        if counter is None:
            counter = 0

        while counter < len(unknowns):
            # print "current location is %d"%counter
            curr = unknowns[counter]
            counter = counter + 1
            if not curr.solved:
                print "variable on blackboard: %s" % curr.symbol
                tick.blackboard.set("counter", counter)
                tick.blackboard.set("curr_unk", curr)
                return b3.SUCCESS

        if counter >= len(unknowns):
            counter = 0
        tick.blackboard.set("counter", counter)
        tick.blackboard.set("curr_unk", unknowns[counter])
        return b3.SUCCESS
        # print "current location is %d"%counter

        # curr = unknowns[counter//len(unknowns)]

        # curr_round = 0
        # while curr.solved and curr_round < len(unknowns):
        #     counter = counter + 1
        #     curr_round = curr_round + 1
        #     curr = unknowns[counter//len(unknowns)]

        # if found a unknown that's unsolved
        # before looping a whole circle
        # if not(curr.solved):
        #     print "variable on blackboard: %s"%curr.symbol
        #     tick.blackboard.set("counter", counter)
        #     tick.blackboard.set("curr_unk", curr)
        #     return b3.SUCCESS
        # else:
        #     return b3.FAILURE
        # if counter >= len(unknowns):
        #     counter = 0
        #     while counter < len(unknowns):
        #         if unknowns[counter].solved:
        #             counter = counter + 1
        #         curr = unknowns[counter]
        #     if counter == len(unknowns):
        #         curr = unknowns[0]
        #tick.blackboard.set("counter", counter)
        #tick.blackboard.set("curr_unk", curr)

        # this scheme will put unsolved variable on the top of the list over blackboard over and over
        # for unk in unknowns:
        # #only load variable that's not currently on, avoid stuck situation
        # if not unk.solved and (curr != unk):
        # print "variable on blackboard: %s"%unk.symbol
        # tick.blackboard.set("curr_unk", unk)
        # return b3.SUCCESS

        # return b3.SUCCESS
