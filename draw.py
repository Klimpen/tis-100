
class Draw:

    def draw(self, core):
        output = []
        output.append(".----------------------.")
        for i in range(0,16):
            if i >= len(core.memory_program):
                output.append(f"| {self.draw_decode(00000000000)} |")
            if output[i].count("IMM")>0:
                output.append(f"| {core.memory_program[i].value:<20} |")
            elif i == core.program_counter:
                output.append(f"| \033[7m{self.draw_decode(core.memory_program[i].value)}\033[27m |")
            else:
                output.append(f"| {self.draw_decode(core.memory_program[i].value)} |")
        output.append("*----------------------*")

        output[0] += f"------."
        output[1] += f"  PC  |"
        output[2] += f"{f" {core.program_counter} |":>7}"
        output[3] += f"------*"
        output[4] += f"  ACC |"
        output[5] += f"{f" {core.acc.value} |":>7}"
        output[6] += f"------*"
        output[7] += f"  BAK |"
        output[8] += f"{f" {core.bak.value} |":>7}"
        output[9] += f"------*"
        output[10] += f"RESULT|"
        output[11] += f"{f" {core.result} |":>7}"
        output[12] += f"------*"
        output[13] += f"   MA |"
        output[14] += f"{f" {core.memory_address} |":>7}"
        output[15] += f"------*"
        output[16] += f"      |"
        output[17] += f"------*"

        return output

    def draw_decode(self, value):
        
        instruction = (value >> 8) & 0b111
        dst         = (value >> 4) & 0b0001111
        src         = (value & 0b00000001111)

        instruction_name = self.name_instruction(instruction)
        dst_name = self.name_address(dst)
        src_name = self.name_address(src)

        output = f"{instruction_name} {dst_name} {src_name}"
        if output == "MOV NIL NIL":
            output = ""
        return f"{f"{output}":<20}"

    def name_instruction(self, instruction):
        match(instruction):
            case 0b000: return "MOV"
            case 0b001: return "HAS"
            case 0b010: return "BSL"
            case 0b011: return "CMP"
            
            case 0b100: return "ADD"
            case 0b101: return "XOR"
            case 0b110: return "JEZ"
            case 0b111: return "JGZ"

    def name_address(self, address):
        match(address):
            case 0b0000: return "NIL"
            case 0b0001: return "ACC"
            case 0b0010: return "BAK"
            case 0b0011: return "IMM"
            
            case 0b0100: return "LEFT"
            case 0b0101: return "RIGHT"
            case 0b0110: return "UP"
            case 0b0111: return "DOWN"
            
            case 0b1000: return "ANY"
            case 0b1001: return "LAST"
            case 0b1010: return "ALL"
            case 0b1011: return "IO"
            
            case 0b1100: return "PC"
            case 0b1101: return "PM"
            case 0b1110: return "MB"
            case 0b1111: return "MA"