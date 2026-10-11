import hashlib
import struct
from pathlib import Path

from Crypto.Cipher import AES

def bl31_parts(data, key, iv):
    marker = data.index(b"EBHEEBRS")
    start = marker + 0x20
    expected = data[marker - 0x20:marker]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    digest = hashlib.sha256()
    for end in range(start + 16, len(data) + 1, 16):
        digest.update(cipher.decrypt(data[end - 16:end]))
        if digest.digest() == expected:
            yield start, end, (start, end, marker - 0x20, key, iv)
            return
    raise ValueError("BL31 encrypted area not found")

def el3_parts(data, key, iv):
    header = struct.unpack_from("<Q", data, 4)[0]
    source, destination, start, end = struct.unpack_from("<4I", data, header + 4)
    start, end = start - source, end - destination
    yield start, end, (start, end, header + 20, key, iv)

def cm_parts(data, key, iv):
    offset = 0
    while offset + 0x40 <= len(data) and struct.unpack_from("<I", data, offset)[0] == 0x10ADAB1E:
        size = struct.unpack_from("<I", data, offset + 4)[0]
        if size < 0x40 or offset + size > len(data):
            raise ValueError("Invalid CM record size")
        record = data[offset:offset + size]
        area = None
        if record[0x28]:
            start, end = struct.unpack_from("<2I", record, 0x44)
            material = AES.new(key, AES.MODE_CBC, iv).decrypt(record[0x4C:0x7C])
            record_iv = bytes(a ^ b for a, b in zip(material[32:], record[0xEC:0xFC]))
            area = offset + start, offset + end, offset + 0x7C, material[:32], record_iv
        yield offset, offset + size, area
        offset += size

def crypt_file(parts, key, iv, path, decrypt):
    path = Path(path)
    directory = path.with_suffix("")
    data = bytearray(path.read_bytes())
    layout = list(parts(data, bytes.fromhex(key), bytes.fromhex(iv)))
    if not layout:
        raise ValueError(f"No image pieces found: {path}")
    files = [("head.bin", 0, layout[0][0])]
    files += [(f"{i}.bin", start, end) for i, (start, end, _) in enumerate(layout)]
    files += [("tail.bin", layout[-1][1], len(data))]
    files = [(name, start, end) for name, start, end in files if start < end]
    if not decrypt:
        for name, start, end in files:
            piece = (directory / name).read_bytes()
            if len(piece) != end - start:
                raise ValueError(f"Changed piece size: {directory / name}")
            data[start:end] = piece
    for _, _, area in layout:
        if area is None:
            continue
        start, end, digest_offset, area_key, area_iv = area
        if not 0 <= start < end <= len(data) or (end - start) % 16:
            raise ValueError(f"Invalid AES area: {path}")
        block = bytes(data[start:end])
        if not decrypt:
            data[digest_offset:digest_offset + 32] = hashlib.sha256(block).digest()
        cipher = AES.new(area_key, AES.MODE_CBC, area_iv)
        data[start:end] = cipher.decrypt(block) if decrypt else cipher.encrypt(block)
    if decrypt:
        directory.mkdir(exist_ok=True)
        for name, start, end in files:
            (directory / name).write_bytes(data[start:end])
    else:
        path.write_bytes(data)
