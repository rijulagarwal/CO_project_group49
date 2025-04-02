registers = {
    "x0": 0, "x1": 0, "x2": 0, "x3": 0, "x4": 0, "x5": 0, "x6": 0, "x7": 0,
    "x8": 0, "x9": 0, "x10": 0, "x11": 0, "x12": 0, "x13": 0, "x14": 0, "x15": 0,
    "x16": 0, "x17": 0, "x18": 0, "x19": 0, "x20": 0, "x21": 0, "x22": 0, "x23": 0,
    "x24": 0, "x25": 0, "x26": 0, "x27": 0, "x28": 0, "x29": 0, "x30": 0, "x31": 0
}
def sext(imm):
    if (imm & 0b100000000000):
        sext_imm = imm | 0b11111111111111111111000000000000
    else:
        sext_imm = imm
    return sext_imm
def add(rs1,rs2):
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
def srl(rd, rs1, rs2):
    shift_amount = rs2 & 0b11111  
    rd = rs1 >> shift_amount
    return rd
'''def lw(imm,rs1)
def jalr(x6,offset)'''
def addi(rs,imm):
    rd = rs + sext(imm)
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
