# import sys
# import os

# input_file = sys.argv[1]
# output_file = sys.argv[2]

def twos_complement(value: int, bit_width: int) -> str:
    if value < 0:
        value = (1 << bit_width) + value
    return format(value & ((1 << bit_width) - 1), f'0{bit_width}b')

registers = {
    "x0": 0, "x1": 0, "x2": 380, "x3": 0, "x4": 0, "x5": 0, "x6": 0, "x7": 0,
    "x8": 0, "x9": 0, "x10": 0, "x11": 0, "x12": 0, "x13": 0, "x14": 0, "x15": 0,
    "x16": 0, "x17": 0, "x18": 0, "x19": 0, "x20": 0, "x21": 0, "x22": 0, "x23": 0,
    "x24": 0, "x25": 0, "x26": 0, "x27": 0, "x28": 0, "x29": 0, "x30": 0, "x31": 0
}
def signed_bin_to_int(b):  
    n = len(b)  
    x = int(b, 2)  
    return x - (1 << n) if b[0] == '1' else x  
def convert_bin_to_register(asm):
    return ("x"+str(int(asm,2)))
             

mapping_registers_to_memory_address={
    "x1": "0x00000104",
    "x2": "0x00000108",
    "x3": "0x0000010C",
    "x4": "0x00000110",
    "x5": "0x00000114",
    "x6": "0x00000118",
    "x7": "0x0000011C",
    "x8": "0x00000120",
    "x9": "0x00000124",
    "x10": "0x00000128",
    "x11": "0x0000012C",
    "x12": "0x00000130",
    "x13": "0x00000134",
    "x14": "0x00000138",
    "x15": "0x0000013C",
    "x16": "0x00000140",
    "x17": "0x00000144",
    "x18": "0x00000148",
    "x19": "0x0000014C",
    "x20": "0x00000150",
    "x21": "0x00000154",
    "x22": "0x00000158",
    "x23": "0x0000015C",
    "x24": "0x00000160",
    "x25": "0x00000164",
    "x26": "0x00000168",
    "x27": "0x0000016C",
    "x28": "0x00000170",
    "x29": "0x00000174",
    "x30": "0x00000178",
    "x31": "0x0000017C"
}

stack_memory_address_value = {
    "0x00000100": 0,
    "0x00000104": 0,
    "0x00000108": 0,
    "0x0000010C": 0,
    "0x00000110": 0,
    "0x00000114": 0,
    "0x00000118": 0,
    "0x0000011C": 0,
    "0x00000120": 0,
    "0x00000124": 0,
    "0x00000128": 0,
    "0x0000012C": 0,
    "0x00000130": 0,
    "0x00000134": 0,
    "0x00000138": 0,
    "0x0000013C": 0,
    "0x00000140": 0,
    "0x00000144": 0,
    "0x00000148": 0,
    "0x0000014C": 0,
    "0x00000150": 0,
    "0x00000154": 0,
    "0x00000158": 0,
    "0x0000015C": 0,
    "0x00000160": 0,
    "0x00000164": 0,
    "0x00000168": 0,
    "0x0000016C": 0,
    "0x00000170": 0,
    "0x00000174": 0,
    "0x00000178": 0,
    "0x0000017C": 0
}

data_memory_value_address={
    "0x00010000": 0,
    "0x00010004": 0,
    "0x00010008": 0,
    "0x0001000C": 0,
    "0x00010010": 0,
    "0x00010014": 0,
    "0x00010018": 0,
    "0x0001001C": 0,
    "0x00010020": 0,
    "0x00010024": 0,
    "0x00010028": 0,
    "0x0001002C": 0,
    "0x00010030": 0,
    "0x00010034": 0,
    "0x00010038": 0,
    "0x0001003C": 0,
    "0x00010040": 0,
    "0x00010044": 0,
    "0x00010048": 0,
    "0x0001004C": 0,
    "0x00010050": 0,
    "0x00010054": 0,
    "0x00010058": 0,
    "0x0001005C": 0,
    "0x00010060": 0,
    "0x00010064": 0,
    "0x00010068": 0,
    "0x0001006C": 0,
    "0x00010070": 0,
    "0x00010074": 0,
    "0x00010078": 0,
    "0x0001007C": 0
}

def sext(imm):
    if (imm & 0b100000000000):
        sext_imm = imm | 0b11111111111111111111000000000000
    else:
        sext_imm = imm
    return sext_imm
def add(rs1,rs2): #Note : whenever we are returning rd, we need to update the value of rd to the value that is being returned
    rd = rs1+rs2
    return rd;
def sub(rs1,rs2):
    rd = rs1-rs2
    return rd
def slt(rs1,rs2):
    if rs1<rs2:
        return 1
    return 0
def Or(rs1,rs2):
    rd=rs1|rs2
    return rd
def And(rs1,rs2):
    rd=rs1&rs2
    return rd
def srl(rs1, rs2):
    shift_amount = rs2 & 0b11111  
    rd = rs1 >> shift_amount
    return rd

#print(format(32,"08x"))

def mem(address_integer):
    address_hex = ("0x"+format(address_integer,"08X"))
    if address_integer<=380:
        return stack_memory_address_value[address_hex]
    return  data_memory_value_address[address_hex]
def lw(imm,rs1): #rd = sext(mem(rs1 + sext(imm[11:0])))
    rd = sext(mem(rs1+imm))
    return rd
def jalr(x6,offset):
    global PC
    rd = PC+4
    #print(x6,offset,x6+offset)
    PC = (x6 + sext(offset)) & ~1
    #print(PC)
    PC-=4
    return rd
def addi(rs,imm): 
    rd = rs + sext(imm)
    return rd
def sw(rs1,imm): #Note : update the value at this memory address to the value in rs2 
    memory_address = rs1 + imm
    #print("check here",memory_address)
    #return ("0x"+format(memory_address,"08X"))
    return memory_address
def beq(rs1,rs2,imm): #Note : this returns the value by which the PC should be updated
    if sext(rs1)==sext(rs2):
        return (sext(imm))
    return 4
def bne(rs1,rs2,imm): #Note : this returns the value by which the PC should be updated
    if sext(rs1)!=sext(rs2):
        return (sext(imm))
    return 4
def jal(imm): 
    global PC
    rd = PC+4
    PC = (PC + (sext((imm)))) & ~1
    PC-=4
    return rd






def function(bin):
    if len(bin)!=32:
        raise  ValueError("Assembly COde must be 32 bits long")
        
    opcode=bin[25:32]
    iset={}
    iset["opcode"]=opcode
    if opcode=="0110011":
        iset["Instruction"]="R"
        iset["rd"]=bin[20:25]
        iset["rs1"]=bin[12:17]
        iset["rs2"]=bin[7:12]
        iset["func7"]=bin[0:7]
        iset["func3"]=bin[17:20]
        if iset['func7']=="0000000" and iset["func3"]=="000":
            iset["sub_type"]="add"
        elif iset['func7']=="0100000" and iset["func3"]=="000":
            iset["sub_type"]="sub"
        elif iset['func7']=="0000000" and iset["func3"]=="010":
            iset["sub_type"]="slt"
        elif iset['func7']=="0000000" and iset["func3"]=="101":
            iset["sub_type"]="srl"
        elif iset['func7']=="0000000" and iset["func3"]=="110":
            iset["sub_type"]="or"
        elif iset['func7']=="0000000" and iset["func3"]=="111":
            iset["sub_type"]="and"
    
    elif opcode in ["0000011","0010011","1100111"]:
        iset["Instruction"]="I"
        iset["imm"]=bin[0:12]
        iset["rs1"]=bin[12:17]
        iset["func3"]=bin[17:20]
        iset["rd"]=bin[20:25]
        if opcode=="0000011" and iset["func3"]=="010":
            iset["sub_type"]="lw"
        elif opcode=="0010011" and iset["func3"]=='000':
            iset["sub_type"]="addi"
        elif opcode=="1100111" and iset["func3"]=='000':
            iset["sub_type"]="jalr"

    elif opcode=="0100011":
        iset["Instruction"]="S"
        iset["rs1"]=bin[12:17]
        iset["rs2"]=bin[7:12]
        iset["imm"]=bin[0:7]+bin[20:25]
        iset["sub_type"]="sw"
        iset['func3']=bin[17:20]
    
    elif opcode=="1100011":
        iset["Instruction"]="B"
        iset["func3"]=bin[17:20]
        iset["rs1"]=bin[12:17]
        iset["rs2"]=bin[7:12]
        iset["imm"]=bin[0]+bin[24]+bin[1:7]+bin[20:24]+"0"
        if iset["func3"]=="000":
            iset["sub_type"]="beq"
        elif iset["func3"]=="001":
            iset["sub_type"]="bne"
        elif iset["func3"]=="100":
            iset["sub_type"]='blt'

    elif opcode=="1101111":
        iset["Instruction"]="J"
        iset["sub_type"]="jal"
        iset['rd']=bin[20:25]
        iset["imm"]=bin[0]+bin[12:20]+bin[11]+bin[1:11]+"0"
    return iset

'''with open (input_file,'r') as file:
    fp = open (output_file,"w")
    read = file.readlines()'''

# file = open(input_file,"r")
fp = open("lodu.txt","w")
# read = file.readlines()
read = ["00000000000100000000000010010011",
"00000000100000000000111000010011",
"00000000100011100000001011100111",
"00000000001000000000000100010011",
"01000000000000000000000100010011",
"00000000001000010000000100110011",
"00000000001000010000000100110011",
"00000000001000010000000100110011",
"00000000001000010000000100110011",
"00000000001000010000000100110011",
"00000000001000010000000100110011",
"00000000000000010010001000000011",
"00000001110000010010000000100011",
"00000000000000010010001000000011",
"00000001110000010010001000100011",
"11100011100011100000111000111000",
"00000000000000000000000001100011"]
readnew=[]
for i in read:
    if "\n" in i:
        readnew.append(i[:-1])
    else:
        readnew.append(i)
Program_Counter_Instruction_Mapping={}
for i in range(len(readnew)):
    Program_Counter_Instruction_Mapping[4*i]=readnew[i]
#print(Program_Counter_Instruction_Mapping)
PC=0
cnt=0
while True:
    cnt+=1
    if cnt==100:
        break
    current_instruction = Program_Counter_Instruction_Mapping[PC]
    #print(current_instruction)
    if current_instruction=="00000000000000000000000001100011": #virtual halt
        fp.write("0b"+twos_complement(PC,32)+" ")
        for i in registers:
            fp.write("0b"+twos_complement(registers[i],32)+' ')
        fp.write("\n")
        break
    elif current_instruction=="11100011100011100000111000111000": #halt
        fp.write("0b"+twos_complement(PC,32)+" ")
        for i in registers:
            fp.write("0b"+twos_complement(registers[i],32)+' ')
        fp.write("\n")
        break
    elif current_instruction=="00001111000011110000111100001111": #RST
        fp.write("0b"+twos_complement(PC,32)+" ")
        for i in registers:
            if i!="x2":
                registers[i]=0
            else:
                registers[i]=380
            fp.write("0b"+twos_complement(registers[i],32)+' ')
        fp.write("\n")
    instruction_set = function(current_instruction)
    #print(instruction_set)
    #print(instruction_set["opcode"])
    instruction = instruction_set["sub_type"]
    '''if opcode=="0110011":
            iset["Instruction"]="R"
            iset["rd"]=bin[20:25]
            iset["rs1"]=bin[12:17]
            iset["rs2"]=bin[7:12]
            iset["func7"]=bin[0:7]
            iset["func3"]=bin[17:20]'''
    if instruction_set["opcode"]=="0110011":
        rd = convert_bin_to_register(instruction_set["rd"])
        rs1 = convert_bin_to_register(instruction_set["rs1"])
        rs2 = convert_bin_to_register(instruction_set["rs2"])
        if instruction=="add":
            registers[rd] = add(registers[rs1],registers[rs2])
        elif instruction=="sub":
            registers[rd] = sub(registers[rs1],registers[rs2])
        elif instruction=="slt":
            registers[rd] = slt(registers[rs1],registers[rs2])
        elif instruction=="srl":
            registers[rd] = srl(registers[rs1],registers[rs2])
        elif instruction=="or":
            registers[rd] = Or(registers[rs1],registers[rs2])
        elif instruction=="and":
            registers[rd] = And(registers[rs1],registers[rs2])
    elif instruction_set["opcode"]=="0000011":
        rd = convert_bin_to_register(instruction_set["rd"])
        rs1 = convert_bin_to_register(instruction_set["rs1"])
        imm = signed_bin_to_int(instruction_set["imm"])
        registers[rd]= lw(imm,registers[rs1])
    elif instruction_set["opcode"]=="0010011":
        rd = convert_bin_to_register(instruction_set["rd"])
        rs1 = convert_bin_to_register(instruction_set["rs1"])
        imm = signed_bin_to_int(instruction_set["imm"])
        #print("this is registers[rd] before:", registers[rd])
        registers[rd]= addi(registers[rs1],imm)
        #print("this is registers[rd] after:", registers[rd])
    elif instruction=="jalr":
        rs1=convert_bin_to_register(instruction_set["rs1"])
        rd = convert_bin_to_register(instruction_set["rd"])
        imm = signed_bin_to_int(instruction_set["imm"])
        registers[rd]=jalr(registers[rs1],imm)
    elif instruction=="sw":
        #"0x"+format(memory_address,"08X"
        imm = signed_bin_to_int(instruction_set["imm"])
        rs1 = convert_bin_to_register(instruction_set["rs1"])
        rs2 = convert_bin_to_register(instruction_set["rs2"])
        if sw(registers[rs1],imm) <=380:
            stack_memory_address_value["0x"+format(sw(registers[rs1],imm),"08X")]=registers[rs2]
        else:
            data_memory_value_address["0x"+format(sw(registers[rs1],imm),"08X")]=registers[rs2]
    elif instruction_set["opcode"]=="1100011":
        imm = signed_bin_to_int(instruction_set["imm"])
        rs1 = registers[convert_bin_to_register(instruction_set["rs1"])]
        rs2 = registers[convert_bin_to_register(instruction_set["rs2"])]
        if instruction == "beq":
            PC+=beq(rs1,rs2,imm)-4
        elif instruction == "bne":
            PC+=bne(rs1,rs2,imm)-4
    elif instruction=="jal":
        rd=convert_bin_to_register(instruction_set["rd"])
        imm = int(instruction_set["imm"],2)
        registers[rd]=jal(imm)
    PC+=4
    registers["x0"]=0
    fp.write("0b"+twos_complement(PC,32)+" ")
    for i in registers:
        fp.write("0b"+twos_complement(registers[i],32)+' ')
    fp.write("\n")
    #print(registers," \n PC is ",PC)
for i in data_memory_value_address:
    #print(type(i),i)
    fp.write(i+":"+("0b"+twos_complement(data_memory_value_address[i],32)))
    fp.write("\n")
#print(registers)
#print()
#print(data_memory_value_address)
