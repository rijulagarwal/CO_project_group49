def twos_complement(value: int, bit_width: int) -> str:
    if value < 0:
        value = (1 << bit_width) + value
    return format(value & ((1 << bit_width) - 1), f'0{bit_width}b')

typeofinstruction={"add":"R","sub":"R","slt":"R","srl":"R","or":"R","and":"R",
                   "lw":"I","addi":"I","jalr":"I",
                   "sw":"S",
                   "beq":"B","bne":"B","blt":"B",
                   "jal":"J"}
instruction_map = {
    "add": ["0000000", "000", "0110011"],
    "sub": ["0100000", "000", "0110011"],
    "slt": ["0000000", "010", "0110011"],
    "srl": ["0000000", "101", "0110011"],
    "or":  ["0000000", "110", "0110011"],
    "and": ["0000000", "111", "0110011"],
    "lw":    ["010", "0000011"],
    "addi":  ["000", "0010011"],
    "jalr":  ["000", "1100111"],
    "sw": ["010","0100011"],
    "beq": ["000", "1100011"],
    "bne": ["001", "1100011"],
    "blt": ["100", "1100011"],
    "jal":"1101111"
}
register_encoding = {
    "zero": "00000",
    "ra": "00001",   
    "sp": "00010",   
    "sp": "00011",   
    "tp": "00100",   
    "t0": "00101",   
    "t1": "00110",   
    "t2": "00111",   
    "s0": "01000", 
    "fp":"010000", 
    "s1": "01001",   
    "a0": "01010",   
    "a1": "01011",   
    "a2": "01100",   
    "a3": "01101",   
    "a4": "01110",   
    "a5": "01111",   
    "a6": "10000",   
    "a7": "10001",   
    "s2": "10010",   
    "s3": "10011",   
    "s4": "10100",   
    "s5": "10101",   
    "s6": "10110",   
    "s7": "10111",   
    "s8": "11000",  
    "s9": "11001",
    "s10": "11010", 
    "s11": "11011",   
    "t3": "11100",   
    "t4": "11101",   
    "t5": "11110",   
    "t6": "11111"    
}


with open ("C:/Users/rijul/c compiler/python/instructions.txt.txt",'r') as file:
    read = file.readlines()
    for line in read:
        instruction=line.split()[0]
        instruction_type=typeofinstruction[instruction]
        if instruction_type=="R":
            registers=line.split()[1].split(",")
            destinationregister=registers[0]
            source_register1=registers[1]
            source_register2=registers[2]
            funct7=instruction_map[instruction][0]
            funct3=instruction_map[instruction][1]
            opcode=instruction_map[instruction][2]
            print(funct7,register_encoding[source_register2],register_encoding[source_register1],funct3,register_encoding[destinationregister],opcode)
            print(line)
            print(line.split())
            print(registers)
        elif instruction_type=="I":
            registers=line.split()[1].split(',')
            return_address_register=registers[0]
            source_register1=registers[1]
            immediate= twos_complement(int(registers[2]),12)
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            print(immediate,register_encoding[source_register1],funct3,register_encoding[return_address_register],opcode)
            print(registers)
            print()
        elif instruction_type=="B":
            registers=line.split()[1].split(',')
            source_register1=registers[0]
            source_register2=registers[1]
            immediate= twos_complement(int(registers[2]),12)
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            print(immediate[:7],register_encoding[source_register2],register_encoding[source_register1],funct3,immediate[7:],opcode)








