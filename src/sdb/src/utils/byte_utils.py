def extract_byte (packet, offset):
    return packet[offset], offset + 1

def extract_short (packet: bytearray, offset):
    return (int(packet[offset]) << 8) | int(packet[offset + 1]), offset + 2

def extract_int (packet: bytearray, offset):
    return (int(packet[offset]) << 24) | (int(packet[offset + 1]) << 16) | (int(packet[offset + 2]) << 8) | (int(packet[offset + 3])), offset + 4
