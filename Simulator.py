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
