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
    "gp": "00011",   
    "tp": "00100",   
    "t0": "00101",   
    "t1": "00110",   
    "t2": "00111",   
    "s0": "01000", 
    "fp": "01000", 
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
with open ("python/instructions.txt",'r') as file:
    fp = open ("output.txt","w")
    read = file.readlines()
    labels={}
    line_number=0
    error=0
    for line in read:
        line_number+=1
        if len(line.split())==3:
                if line.split()[0][-1]==":":
                    label=line.split()[0][:-1]
                    print(label)
                    labels[label]=line_number
                else:
                    error=1
                    print(line.split()[1])
                    break
                instruction=line.split()[1]
                registers=line.split()[2].split(',')
        elif len(line.split())==2:
            instruction=line.split()[0]
            registers=line.split()[1].split(",")
        else:
             error=1
             break
        instruction_type=typeofinstruction[instruction]
        if instruction_type=="R":      
                destinationregister=registers[0]
                source_register1=registers[1]
                source_register2=registers[2]
                funct7=instruction_map[instruction][0]
                funct3=instruction_map[instruction][1]
                opcode=instruction_map[instruction][2]
                print(funct7,register_encoding[source_register2],register_encoding[source_register1],funct3,register_encoding[destinationregister],opcode,sep='')
        elif instruction_type=="I":
            if len(registers)==3:
                    return_address_register=registers[0]
                    source_register1=registers[1]
                    try:
                         immediate= twos_complement(int(registers[2]),12)
                    except ValueError:
                         immediate_label= registers[2]
                         if immediate_label in labels:
                              immediate=twos_complement((labels[immediate_label]-line_number)*4,12)
                    funct3=instruction_map[instruction][0]
                    opcode=instruction_map[instruction][1]
                    print(immediate,register_encoding[source_register1],funct3,register_encoding[return_address_register],opcode,sep='')
            elif len(registers)==2:
                return_address_register=registers[0]
                immediate=twos_complement(int(registers[1].split("(")[0]),12)
                source_register1=registers[1].split("(")[1][:-1]
                funct3=instruction_map[instruction][0]
                opcode=instruction_map[instruction][1]
                print(immediate,register_encoding[source_register1],funct3,register_encoding[return_address_register],opcode,sep='')
        elif instruction_type=="B":
            source_register1=registers[0]
            source_register2=registers[1]
            try:
                    immediate= twos_complement(int(registers[2]),13)
            except ValueError:
                    immediate_label= registers[2]
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,13)
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            print(immediate[0],immediate[2:8],register_encoding[source_register2],register_encoding[source_register1],funct3,immediate[8:12],immediate[1],opcode,sep='')
        elif instruction_type=="S":
            data_register=registers[0]
            immediate=twos_complement(int(registers[1].split("(")[0]),12)
            source_address_register=registers[1].split("(")[1][:-1]
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            print(immediate[:7],register_encoding[data_register],register_encoding[source_address_register],funct3,immediate[7:],opcode,sep='')
            
        elif instruction_type=="J":
            destinationregister=registers[0]
            immediate=twos_complement(int(registers[1]),21)
            opcode=instruction_map[instruction]
            print(immediate[0],immediate[10:20],immediate[9],immediate[1:9],register_encoding[destinationregister],opcode,sep='')






