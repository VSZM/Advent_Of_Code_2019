from abc import ABC, abstractmethod
from typing import List
import sys

POSITION_MODE = 0
VALUE_MODE = 1

class State(object):

    def __init__(self, memory, ip):
        self.memory = memory
        self.ip = ip

class InstructionBase(ABC):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None, operand3 = None,  operand3_mode = POSITION_MODE):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
        self.operand1_mode = operand1_mode
        self.operand2_mode = operand2_mode
        self.operand3_mode = operand3_mode

    @abstractmethod
    def operate(self, state: State) -> State:
        pass

class IOInstruction(InstructionBase):

    def __init__(self, operand1, operand1_mode = None):
        super().__init__(operand1, operand1_mode)

class UnaryInstruction(InstructionBase):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None):
        super().__init__(operand1, operand1_mode, operand2, operand2_mode)


class BinaryInstruction(InstructionBase):

    def __init__(self, operator, operand1, operand1_mode = None, operand2 = None, operand2_mode = None, operand3 = None,  operand3_mode = POSITION_MODE):
        super().__init__(operand1, operand1_mode, operand2, operand2_mode, operand3, operand3_mode)
        self.operator = operator

    def operate(self, state: State) -> State:
        memory = state.memory
        if self.operand1_mode == POSITION_MODE:
            a = memory[memory[self.operand1]]
        else:
            a = memory[self.operand1]
        
        if self.operand2_mode == POSITION_MODE:
            b = memory[memory[self.operand2]]
        else:
            b = memory[self.operand2]
        
        value = self.operator(a, b)
        if self.operand3_mode == POSITION_MODE:
            memory[memory[self.operand3]] = value
        else:
            memory[self.operand3] = value
        
        state.ip += 4
        return state

class ReadInput(IOInstruction):

    
    def __init__(self, operand1, input_num):
        super().__init__(operand1)
        self.input_num = input_num

    def operate(self, state: State) -> State:
        state.memory[state.memory[self.operand1]] = self.input_num
        state.ip += 2
        return state
    
    def __str__(self):
        d = vars(self).copy()
        return f'ReadInput |{d}|\n'

    __repr__ = __str__

class PrintOutput(IOInstruction):

    
    def __init__(self, operand1, operand1_mode):
        super().__init__(operand1, operand1_mode)

    def operate(self, state: State) -> State:
        memory = state.memory
        if self.operand1_mode == POSITION_MODE:
            print(memory[memory[self.operand1]])
        else:
            print(memory[self.operand1])

        state.ip += 2
        return state
    
    def __str__(self):
        d = vars(self).copy()
        return f'PrintOutput |{d}|\n'

    __repr__ = __str__

class Add(BinaryInstruction):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None, operand3 = None,  operand3_mode = POSITION_MODE):
        operator = lambda x, y: x + y
        super().__init__(operator, operand1, operand1_mode, operand2, operand2_mode, operand3, operand3_mode)

    def __str__(self):
        d = vars(self).copy()
        del d['operator']
        return f'Add |{d}|\n'

    __repr__ = __str__

class Multiply(BinaryInstruction):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None, operand3 = None,  operand3_mode = POSITION_MODE):
        operator = lambda x, y: x * y
        super().__init__(operator, operand1, operand1_mode, operand2, operand2_mode, operand3, operand3_mode)


    def __str__(self):
        d = vars(self).copy()
        del d['operator']
        return f'Multiply |{d}|\n'

    __repr__ = __str__


class JumpNonZero(UnaryInstruction):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None):
        super().__init__(operand1, operand1_mode, operand2, operand2_mode)

    def operate(self, state: State) -> State:
        memory = state.memory
        if self.operand1_mode == POSITION_MODE:
            expr = memory[memory[self.operand1]]
        else:
            expr = memory[self.operand1]
        
        if self.operand2_mode == POSITION_MODE:
            pos = memory[memory[self.operand2]]
        else:
            pos = memory[self.operand2]

        if expr:
            state.ip = pos
        else:
            state.ip += 3

        return state

    def __str__(self):
        d = vars(self).copy()
        return f'JumpNonZero |{d}|\n'

    __repr__ = __str__

class JumpZero(UnaryInstruction):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None):
        super().__init__(operand1, operand1_mode, operand2, operand2_mode)

    def operate(self, state: State) -> State:
        memory = state.memory
        if self.operand1_mode == POSITION_MODE:
            expr = memory[memory[self.operand1]]
        else:
            expr = memory[self.operand1]
        
        if self.operand2_mode == POSITION_MODE:
            pos = memory[memory[self.operand2]]
        else:
            pos = memory[self.operand2]

        if not expr:
            state.ip = pos
        else:
            state.ip += 3

        return state

    def __str__(self):
        d = vars(self).copy()
        return f'JumpZero |{d}|\n'

    __repr__ = __str__
    
class LessThan(BinaryInstruction):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None, operand3 = None,  operand3_mode = POSITION_MODE):
        operator = lambda x, y: int(x < y)
        super().__init__(operator, operand1, operand1_mode, operand2, operand2_mode, operand3, operand3_mode)

    def __str__(self):
        d = vars(self).copy()
        del d['operator']
        return f'LessThan |{d}|\n'

    __repr__ = __str__

class Equals(BinaryInstruction):

    def __init__(self, operand1, operand1_mode = None, operand2 = None, operand2_mode = None, operand3 = None,  operand3_mode = POSITION_MODE):
        operator = lambda x, y: int(x == y)
        super().__init__(operator, operand1, operand1_mode, operand2, operand2_mode, operand3, operand3_mode)

    def __str__(self):
        d = vars(self).copy()
        del d['operator']
        return f'Equals |{d}|\n'

    __repr__ = __str__


def interpretProgram(memory: List[int], input_num) -> List[InstructionBase]:
    instructions = []
    state = State(memory, 0)
    while state.memory[state.ip] != 99:
        memory = state.memory
        ip = state.ip
        if memory[ip] == 3:
            instruction = ReadInput(ip + 1, input_num)
        else:
            opcode = str(memory[ip]).rjust(5, '0')
            mode1 = int(opcode[-3])
            mode2 = int(opcode[-4])
            mode3 = int(opcode[0])
            if opcode[-2:] == '01':
                instruction = Add(ip + 1, mode1, ip + 2, mode2, ip + 3, mode3)
            elif opcode[-2:] == '02':
                instruction = Multiply(ip + 1, mode1, ip + 2, mode2, ip + 3, mode3)
            elif opcode[-2:] == '04':
                instruction = PrintOutput(ip + 1, mode1)
            elif opcode[-2:] == '05':
                instruction = JumpNonZero(ip + 1, mode1, ip + 2, mode2)
            elif opcode[-2:] == '06':
                instruction = JumpZero(ip + 1, mode1, ip + 2, mode2)
            elif opcode[-2:] == '07':
                instruction = LessThan(ip + 1, mode1, ip + 2, mode2, ip + 3, mode3)
            elif opcode[-2:] == '08':
                instruction = Equals(ip + 1, mode1, ip + 2, mode2, ip + 3, mode3)
            else:
                raise ValueError('Invalid state')
        
        instruction.operate(state)
        instructions.append(instruction)

    return instructions


def runProgram(memory: List[int]):
    instructions = interpretProgram(memory, 5)
    print(instructions)


if __name__ == "__main__":
    with open('day5.txt', 'r') as f:
        memory = [int(num) for num in f.readline().split(',')]
        runProgram(memory)