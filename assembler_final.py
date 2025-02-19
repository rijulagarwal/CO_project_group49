import sys
import os

if len(sys.argv) != 3:
    print("Format: python3 Assembler.py <input_assembly_file> <output_machine_code_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if input_file[1:3] == ":\\":
    input_file = input_file.replace("\\", "/").replace("C:/", "/mnt/c/")
if output_file[1:3] == ":\\":
    output_file = output_file.replace("\\", "/").replace("C:/", "/mnt/c/")

if not os.path.exists(input_file):
    print(f"Error: Input file '{input_file}' not found!")
    sys.exit(1)
    
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
with open (input_file,'r') as file:
    fp = open (output_file,"w")
    read = file.readlines()
    final_output=[-1]*1000000
    labels={}
    line_number=0
    error=0
    skipped=[]
    virtual_hault=['beq zero,zero,0','beq zero,zero,0 ','beq zero,zero,0 \n','beq zero,zero,0\n']
    if read[-1] not in virtual_hault:
         error=2
         fp.write("Error:Virtual Hault is not the last instruction")
    for line in read:
        if error==1:
             break
        line_number+=1
        if line=="\n":
             final_output[line_number]=0
             continue
        if len(line.split())==3:
                if line.split()[0][-1]==":":
                    label=line.split()[0][:-1]
                    labels[label]=line_number
                else:
                    error=1
                    print(line.split()[1])
                    break
                instruction=line.split()[1]
                registers=line.split()[2].split(',')
        elif len(line.split())==2:
            if len(line.split()[0].split(":"))==2:
                 label=line.split()[0].split(":")[0]
                 labels[label]=line_number
                 instruction=line.split()[0].split(":")[1]
                 registers=line.split()[1].split(",")
            else:
                instruction=line.split()[0]
                registers=line.split()[1].split(",")
        else:
             error=1
             final_output[0]=line_number
             break
        if instruction not in typeofinstruction:
            error=1
            final_output[0]=line_number
            break
        instruction_type=typeofinstruction[instruction]
        if instruction_type=="R":
                if len(registers)!=3:
                    error=1
                    final_output[0]=line_number
                    break
                destinationregister=registers[0]
                source_register1=registers[1]
                source_register2=registers[2]
                funct7=instruction_map[instruction][0]
                funct3=instruction_map[instruction][1]
                opcode=instruction_map[instruction][2]
                output=''
                output+=funct7
                if source_register1 not in register_encoding:
                    error=1
                    final_output[0]=line_number
                    break
                if source_register2 not in register_encoding:
                    error=1
                    final_output[0]=line_number
                    break
                if destinationregister not in register_encoding:
                    error=1
                    final_output[0]=line_number
                    break
                output+=register_encoding[source_register2]
                output+=register_encoding[source_register1]
                output+=funct3
                output+=register_encoding[destinationregister]
                output+=opcode
                final_output[line_number]=output
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
                         else:
                              skipped.append((line,line_number))
                    funct3=instruction_map[instruction][0]
                    opcode=instruction_map[instruction][1]
                    output=''
                    output+=immediate
                    if source_register1 not in register_encoding:
                         error=1
                         final_output[0]=line_number
                         break
                    output+=register_encoding[source_register1]
                    output+=funct3
                    if return_address_register not in register_encoding:
                         error=1
                         final_output[0]=line_number
                         break
                    output+=register_encoding[return_address_register]
                    output+=opcode
                    final_output[line_number]=output
            elif len(registers)==2:
                return_address_register=registers[0]
                try:
                         immediate=twos_complement(int(registers[1].split("(")[0]),12)
                except ValueError:
                    immediate_label= registers[1].split("(")[0]
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,12)
                    else:
                              skipped.append((line,line_number))
                if len(registers[1].split("("))!=2:
                    error=1
                    final_output[0]=line_number
                    break
                source_register1=registers[1].split("(")[1][:-1]
                funct3=instruction_map[instruction][0]
                opcode=instruction_map[instruction][1]
                output=''
                output+=immediate
                if source_register1 not in register_encoding:
                     error=1
                     final_output[0]=line_number
                     break
                output+=register_encoding[source_register1]
                output+=funct3
                if return_address_register not in register_encoding:
                     error=1
                     final_output[0]=line_number
                     break
                output+=register_encoding[return_address_register]
                output+=opcode
                final_output[line_number]=output
            else:
                 error=1
                 final_output[0]=line_number
                 break
        elif instruction_type=="B":
            if len(registers)!=3:
                 error=1
                 final_output[0]=line_number
                 break
            source_register1=registers[0]
            source_register2=registers[1]
            try:
                    immediate= twos_complement(int(registers[2]),13)
            except ValueError:
                    immediate_label= registers[2]
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,13)
                    else:
                              skipped.append((line,line_number))
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            output=''
            if source_register1 not in register_encoding:
                 error=1
                 final_output[0]=line_number
                 break
            if source_register2 not in register_encoding:
                 error=1
                 final_output[0]=line_number
                 break
            output+=immediate[0]+immediate[2:8]+register_encoding[source_register2]+register_encoding[source_register1]+funct3+immediate[8:12]+immediate[1]+opcode
            final_output[line_number]=output
        elif instruction_type=="S":
            if len(registers)!=2:
                 error=1
                 final_output[0]=line_number
                 break
            data_register=registers[0]
            try:
                    immediate=twos_complement(int(registers[1].split("(")[0]),12)
            except ValueError:
                    immediate_label=registers[1].split("(")[0]
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,12)
                    else:
                        skipped.append((line,line_number))
            if len(registers[1].split("("))!=2:
                 error=1
                 final_output[0]=line_number
                 break
            source_address_register=registers[1].split("(")[1][:-1]
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            output=''
            output+=immediate[:7]
            if data_register not in register_encoding:
                 error=1
                 final_output[0]=line_number 
                 break
            if source_address_register not in register_encoding:
                 error=1
                 final_output[0]=line_number
                 break
            output+=register_encoding[data_register]
            output+=register_encoding[source_address_register]
            output+=funct3
            output+=immediate[7:]
            output+=opcode
            final_output[line_number]=output
        elif instruction_type=="J":
            if len(registers)!=2:
                 error=1
                 final_output[0]=line_number
                 break
            destinationregister=registers[0]
            try:
                    immediate=twos_complement(int(registers[1]),21)
            except ValueError:
                    immediate_label=(registers[1])
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,21)
                    else:
                        skipped.append((line,line_number))
            opcode=instruction_map[instruction]
            output=''
            output+=immediate[0]+immediate[10:20]+immediate[9]+immediate[1:9]+register_encoding[destinationregister]+opcode
            final_output[line_number]=output
    total_lines=line_number
    for tuple in skipped:
         if error==1:
              break
         line = tuple[0]
         line_number=tuple[1]
         if len(line.split())==3:
                instruction=line.split()[1]
                registers=line.split()[2].split(',')
         elif len(line.split())==2:
            if len(line.split()[0].split(":"))==2:
                 instruction=line.split()[0].split(":")[1]
                 registers=line.split()[1].split(",")
            else:
                instruction=line.split()[0]
                registers=line.split()[1].split(",")
         else:
             error=1
             final_output[0]=line_number
             break
         if instruction not in typeofinstruction:
            error=1
            final_output[0]=line_number
            break
         instruction_type=typeofinstruction[instruction]
         if instruction_type=="R":
                if len(registers)!=3:
                    error=1
                    final_output[0]=line_number
                    break
                destinationregister=registers[0]
                source_register1=registers[1]
                source_register2=registers[2]
                funct7=instruction_map[instruction][0]
                funct3=instruction_map[instruction][1]
                opcode=instruction_map[instruction][2]
                output=''
                output+=funct7
                if source_register1 not in register_encoding:
                    error=1
                    final_output[0]=line_number
                    break
                if source_register2 not in register_encoding:
                    error=1
                    final_output[0]=line_number
                    break
                if destinationregister not in register_encoding:
                    error=1
                    final_output[0]=line_number
                    break
                output+=register_encoding[source_register2]
                output+=register_encoding[source_register1]
                output+=funct3
                output+=register_encoding[destinationregister]
                output+=opcode
                final_output[line_number]=output
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
                         else:
                              error=1
                              final_output[0]=line_number
                              break
                    funct3=instruction_map[instruction][0]
                    opcode=instruction_map[instruction][1]
                    output=''
                    output+=immediate
                    if source_register1 not in register_encoding:
                         error=1
                         final_output[0]=line_number
                         break
                    output+=register_encoding[source_register1]
                    output+=funct3
                    if return_address_register not in register_encoding:
                         error=1
                         final_output[0]=line_number
                         break
                    output+=register_encoding[return_address_register]
                    output+=opcode
                    final_output[line_number]=output
            elif len(registers)==2:
                return_address_register=registers[0]
                try:
                         immediate=twos_complement(int(registers[1].split("(")[0]),12)
                except ValueError:
                    immediate_label= registers[1].split("(")[0]
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,12)
                    else:
                        error=1
                        final_output[0]=line_number
                        break
                if len(registers[1].split("("))!=2:
                    error=1
                    final_output[0]=line_number
                    break
                source_register1=registers[1].split("(")[1][:-1]
                funct3=instruction_map[instruction][0]
                opcode=instruction_map[instruction][1]
                output=''
                output+=immediate
                if source_register1 not in register_encoding:
                     error=1
                     final_output[0]=line_number
                     break
                output+=register_encoding[source_register1]
                output+=funct3
                if return_address_register not in register_encoding:
                     error=1
                     final_output[0]=line_number
                     break
                output+=register_encoding[return_address_register]
                output+=opcode
                final_output[line_number]=output
            else:
                 error=1
                 final_output[0]=line_number
                 break
         elif instruction_type=="B":
            if len(registers)!=3:
                 error=1
                 final_output[0]=line_number
                 break
            source_register1=registers[0]
            source_register2=registers[1]
            try:
                    immediate= twos_complement(int(registers[2]),13)
            except ValueError:
                    immediate_label= registers[2]
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,13)
                    else:
                        error=1
                        final_output[0]=line_number
                        break
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            output=''
            if source_register1 not in register_encoding:
                 error=1
                 final_output[0]=line_number
                 break
            if source_register2 not in register_encoding:
                 error=1
                 final_output[0]=line_number
                 break
            output+=immediate[0]+immediate[2:8]+register_encoding[source_register2]+register_encoding[source_register1]+funct3+immediate[8:12]+immediate[1]+opcode
            final_output[line_number]=output
         elif instruction_type=="S":
            if len(registers)!=2:
                 error=1
                 final_output[0]=line_number
                 break
            data_register=registers[0]
            try:
                    immediate=twos_complement(int(registers[1].split("(")[0]),12)
            except ValueError:
                    immediate_label=registers[1].split("(")[0]
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,12)
                    else:
                        error=1
                        final_output[0]=line_number
                        break
            if len(registers[1].split("("))!=2:
                 error=1
                 final_output[0]=line_number
                 break
            source_address_register=registers[1].split("(")[1][:-1]
            funct3=instruction_map[instruction][0]
            opcode=instruction_map[instruction][1]
            output=''
            output+=immediate[:7]
            if data_register not in register_encoding:
                 error=1
                 final_output[0]=line_number
                 break
            if source_address_register not in register_encoding:
                 error=1
                 final_output[0]=line_number
                 break
            output+=register_encoding[data_register]
            output+=register_encoding[source_address_register]
            output+=funct3
            output+=immediate[7:]
            output+=opcode
            final_output[line_number]=output
         elif instruction_type=="J":
            if len(registers)!=2:
                 error=1
                 final_output[0]=line_number
                 break
            destinationregister=registers[0]
            try:
                    immediate=twos_complement(int(registers[1]),21)
            except ValueError:
                    immediate_label=(registers[1])
                    if immediate_label in labels:
                        immediate=twos_complement((labels[immediate_label]-line_number)*4,21)
                    else:
                        error=1
                        final_output[0]=line_number
                        break
            opcode=instruction_map[instruction]
            output=''
            output+=immediate[0]+immediate[10:20]+immediate[9]+immediate[1:9]+register_encoding[destinationregister]+opcode
            final_output[line_number]=output

    if error==0:
        for i in range(total_lines):
            if final_output[i+1]==0:
                 continue
            fp.write(final_output[i+1])
            fp.write("\n")
    elif error==1:
         fp.write(f'Typo/Syntax Error found in line number {final_output[0]}')






