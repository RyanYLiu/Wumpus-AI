# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.turnAround = 0
        self.positionStack = [(1, 1)]
        self.pathBack = []
        self.visitedPositions = set()
        self.leave = False
        self.arrow = 1
        self.facingDirection = 'right'
        self.rightEdge = 0
        self.topEdge = 0
        # self.deadWumpus = False

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        X = self.positionStack[-1][0]
        Y = self.positionStack[-1][1]
        # print(self.positionStack)
        # print(self.visitedPositions)
        # print(self.facingDirection)
        # print(self.topEdge)
        # print(self.rightEdge)

        if self.turnAround:
            # print('turning around')
            # second turn
            if self.turnAround == 1:
                self.turnAround = 2
                return Agent.Action.TURN_RIGHT
            # move after finish turning
            else:
                self.turnAround = 0
                if self.facingDirection == 'up':
                    self.facingDirection = 'down'
                elif self.facingDirection == 'down':
                    self.facingDirection = 'up'
                elif self.facingDirection == 'left':
                    self.facingDirection = 'right'
                else:
                    self.facingDirection = 'left'
                self.visitedPositions.add(self.positionStack.pop())
                return Agent.Action.FORWARD

                # if we perceive roar
        if scream:
            # print('heard scream')
            # move forward
            # self.deadWumpus = 1
            if self.facingDirection == 'up' or self.facingDirection == 'down':
                self.visitedPositions.remove((X + 1, Y))
                self.visitedPositions.remove((X - 1, Y))
            elif self.facingDirection == 'left' or self.facingDirection == 'right':
                self.visitedPositions.remove((X, Y + 1))
                self.visitedPositions.remove((X, Y - 1))

        if self.leave:
            # print('get me outta here')
            if X == 1 and Y == 1:
                return Agent.Action.CLIMB

            if self.facingDirection == 'up':
                forward = (X, Y + 1)
                newRight = 'right'
            elif self.facingDirection == 'down':
                forward = (X, Y - 1)
                newRight = 'left'
            elif self.facingDirection == 'left':
                forward = (X - 1 , Y)
                newRight = 'up'
            else:
                forward = (X + 1 , Y)
                newRight = 'down'

            if forward == self.positionStack[-2]:
                self.visitedPositions.add(self.positionStack.pop())
                return Agent.Action.FORWARD
            else:
                self.facingDirection = newRight
                return Agent.Action.TURN_RIGHT

        if glitter:
            # print('shiny')
            self.leave = True
            return Agent.Action.GRAB

        # if we perceive a breeze
        if breeze:
            # print('woosh you have small penor')
            # check current position and find possible locations of pit
            if X == 1 and Y == 1:
                return Agent.Action.CLIMB
            else:
                # mark positions as dangerous
                if (X + 1, Y) not in self.positionStack:
                    self.visitedPositions.add((X + 1, Y))
                if (X - 1, Y) not in self.positionStack and X - 1 > 0:
                    self.visitedPositions.add((X - 1, Y))
                if (X, Y + 1) not in self.positionStack:
                    self.visitedPositions.add((X, Y + 1))
                if (X, Y - 1) not in self.positionStack and Y - 1 > 0:
                    self.visitedPositions.add((X, Y - 1))

                # start turn around
                self.turnAround = 1
                return Agent.Action.TURN_RIGHT

        # if we perceive a bump
        if bump:
            # print('ding dong')
            self.visitedPositions.add(self.positionStack.pop())
            if self.facingDirection == 'up':
                self.topEdge = Y
            elif self.facingDirection == 'right':
                self.rightEdge = X

            X = self.positionStack[-1][0]
            Y = self.positionStack[-1][1]

            if self.facingDirection == 'up':
                forward = (X,Y+1)
                left = (X-1,Y)
                right = (X+1,Y)
            elif self.facingDirection == 'down':
                forward = (X, Y - 1)
                left = (X + 1, Y)
                right = (X - 1, Y)
            elif self.facingDirection == 'left':
                forward = (X-1, Y)
                left = (X, Y-1)
                right = (X, Y+1)
            else:
                forward = (X+1, Y)
                left = (X, Y+1)
                right = (X, Y-1)

            if self.facingDirection == 'up':
                if self.topEdge != 0 and forward[1] == self.topEdge:
                    self.visitedPositions.add(forward)
                if left[0] == 0:
                    self.visitedPositions.add(left)
                elif right[0] == self.rightEdge and self.rightEdge != 0:
                    self.visitedPositions.add(right)
            elif self.facingDirection == 'down':
                if forward[1] == 0:
                    self.visitedPositions.add(forward)
                if left[0] == self.rightEdge and self.rightEdge != 0:
                    self.visitedPositions.add(left)
                elif right[0] == 0:
                    self.visitedPositions.add(right)
            elif self.facingDirection == 'left':
                if forward[0] == 0:
                    self.visitedPositions.add(forward)
                if left[1] == 0:
                    self.visitedPositions.add(left)
                elif right[1] == self.topEdge and self.topEdge != 0:
                    self.visitedPositions.add(right)
            elif self.facingDirection == 'right':
                if self.rightEdge != 0 and forward[0] == self.rightEdge:
                    self.visitedPositions.add(forward)
                if left[1] == self.topEdge and self.topEdge != 0:
                    self.visitedPositions.add(left)
                elif right[1] == 0:
                    self.visitedPositions.add(right)

        # if we perceive a stench
        if stench and self.arrow:
            self.arrow = 0
            # if self.arrow:
            if self.facingDirection == 'up' or self.facingDirection == 'down':
                self.visitedPositions.add((X + 1, Y))
                self.visitedPositions.add((X - 1, Y))
            elif self.facingDirection == 'left' or self.facingDirection == 'right':
                self.visitedPositions.add((X, Y + 1))
                self.visitedPositions.add((X, Y - 1))
            return Agent.Action.SHOOT

        # if we perceive nothing move forward
        else:
            # print('sense nothing')
            # checkList = [(X + 1, Y), (X - 1, Y), (X, Y + 1), (X, Y - 1)]
            if self.facingDirection == 'up':
                forward = (X,Y+1)
                left = (X-1,Y)
                right = (X+1,Y)
                newLeft = 'left'
                newRight = 'right'
            elif self.facingDirection == 'down':
                forward = (X, Y - 1)
                left = (X + 1, Y)
                right = (X - 1, Y)
                newLeft = 'right'
                newRight = 'left'
            elif self.facingDirection == 'left':
                forward = (X-1, Y)
                left = (X, Y-1)
                right = (X, Y+1)
                newLeft = 'down'
                newRight = 'up'
            else:
                forward = (X+1, Y)
                left = (X, Y+1)
                right = (X, Y-1)
                newLeft = 'up'
                newRight = 'down'

            if self.facingDirection == 'up':
                if self.topEdge != 0 and forward[1] == self.topEdge:
                    self.visitedPositions.add(forward)
                if left[0] == 0:
                    self.visitedPositions.add(left)
                elif right[0] == self.rightEdge and self.rightEdge != 0:
                    self.visitedPositions.add(right)
            elif self.facingDirection == 'down':
                if forward[1] == 0:
                    self.visitedPositions.add(forward)
                if left[0] == self.rightEdge and self.rightEdge != 0:
                    self.visitedPositions.add(left)
                elif right[0] == 0:
                    self.visitedPositions.add(right)
            elif self.facingDirection == 'left':
                if forward[0] == 0:
                    self.visitedPositions.add(forward)
                if left[1] == 0:
                    self.visitedPositions.add(left)
                elif right[1] == self.topEdge and self.topEdge != 0:
                    self.visitedPositions.add(right)
            elif self.facingDirection == 'right':
                if self.rightEdge != 0 and forward[0] == self.rightEdge:
                    self.visitedPositions.add(forward)
                if left[1] == self.topEdge and self.topEdge != 0:
                    self.visitedPositions.add(left)
                elif right[1] == 0:
                    self.visitedPositions.add(right)


            if forward not in self.positionStack and forward not in self.visitedPositions:
                self.positionStack.append(forward)
                return Agent.Action.FORWARD
            elif left not in self.positionStack and left not in self.visitedPositions:
                # print('checking left')
                self.facingDirection = newLeft
                return Agent.Action.TURN_LEFT
            elif right not in self.positionStack and right not in self.visitedPositions:
                # print('checking right')
                self.facingDirection = newRight
                return Agent.Action.TURN_RIGHT
            else:
                # print('nowhere to go')
                if X == 1 and Y == 1:
                    return Agent.Action.CLIMB

                if forward == self.positionStack[-2]:
                    self.visitedPositions.add(self.positionStack.pop())
                    return Agent.Action.FORWARD
                else:
                    self.facingDirection = newRight
                    return Agent.Action.TURN_RIGHT


            # ======================================================================
            # YOUR CODE ENDS
            # ======================================================================

            # ======================================================================
            # YOUR CODE BEGINS
            # ======================================================================


            # ======================================================================
            # YOUR CODE ENDS
            # ======================================================================


