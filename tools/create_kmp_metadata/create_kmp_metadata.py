from argparse import ArgumentParser
from configparser import ConfigParser
from dataclasses import dataclass
import struct


@dataclass
class Metadata:
    disable_oob_in_action: False


# TODO: more robust stream R/W class
def read_u16(bytes):
    return struct.unpack(">H", bytes)[0]


# TODO: more robust stream R/W class
def read_u32(bytes):
    return struct.unpack(">I", bytes)[0]


# TODO: more robust stream R/W class
def write_bool(bytes):
    return struct.pack(">?", bytes)


# TODO: more robust stream R/W class
def write_u8(bytes):
    return struct.pack(">B", bytes)


# TODO: more robust stream R/W class
def write_u16(bytes):
    return struct.pack(">H", bytes)


# TODO: more robust stream R/W class
def write_u32(bytes):
    return struct.pack(">I", bytes)


def validate_file(file) -> bool:
    # We need to guarantee file[:12] at first, because we need to read:
    #   - File signature
    #   - File size
    #   - Section count
    #   - Header size
    if len(file) < 16:
        print("ERROR: File is too small to be read as KMP")
        return False

    signature = read_u32(file[0x0:0x4])
    if signature != 0x524B4D44:
        print("ERROR: Invalid file signature")
        return False

    file_size = read_u32(file[0x4:0x8])
    if file_size != len(file):
        print("ERROR: Size mismatch")
        return False

    section_count = read_u16(file[0x8:0xA])
    header_size = read_u16(file[0xA:0xC])
    offset_base = section_count * 0x4 + 0x10

    if len(file) < offset_base:
        print(f"ERROR: File is too small for all {section_count} sections to exist")
        return False

    if header_size < offset_base:
        print("ERROR: Header reads outside its bounds")
        return False
    elif header_size > offset_base:
        print(
            "WARN: Header is unnecessarily big - if there's extra data here, this patch will not work"
        )

    BASE_SECTION_SIGNATURES = [
        0x4B545054,  # KTPT
        0x454E5054,  # ENPT
        0x454E5048,  # ENPH
        0x49545054,  # ITPT
        0x49545048,  # ITPH
        0x434B5054,  # CKPT
        0x434B5048,  # CKPH
        0x474F424A,  # GOBJ
        0x504F5449,  # POTI
        0x41524541,  # AREA
        0x43414D45,  # CAME
        0x4A475054,  # JGPT
        0x434E5054,  # CNPT
        0x4D535054,  # MSPT
        0x53544749,  # STGI
    ]

    CUSTOM_SECTION_SIGNATURES = [
        0x4D455441,  # META
    ]

    SECTION_SIGNATURES = BASE_SECTION_SIGNATURES + CUSTOM_SECTION_SIGNATURES

    for i in range(section_count):
        bound_start = i * 0x4 + 0x10
        bound_end = bound_start + 0x4
        offset = read_u32(file[bound_start:bound_end])

        if offset >= (file_size - header_size):
            print("ERROR: Offset points out of bounds of file")
            return False

        current_signature = read_u32(
            file[offset + header_size : offset + header_size + 4]
        )

        if current_signature not in SECTION_SIGNATURES:
            print("WARN: Unknown section signature")

    return True


def read_config() -> Metadata:
    config = ConfigParser()
    config.read("./config.ini")

    disable_oob_in_action = config.getboolean("metadata", "disable_oob_in_action")
    return Metadata(disable_oob_in_action)


# TODO
def overwrite_old_metadata(file, metadata: Metadata, file_pos: int):
    return file


def create_new_metadata(file, metadata: Metadata):
    STRUCT_SIZE = 0x4

    file_size = read_u32(file[0x4:0x8])
    header_size = read_u16(file[0xA:0xC])

    # We need room for a new section offset, section header, and entry
    metadata_section_pos = file_size - header_size
    new_file_size = file_size + 0x4 + 0x8 + STRUCT_SIZE
    new_section_count = read_u16(file[0x8:0xA]) + 1
    new_header_size = header_size + 0x4

    new_file = file[:0x4]
    new_file += write_u32(new_file_size)
    new_file += write_u16(new_section_count)
    new_file += write_u16(new_header_size)
    new_file += file[0xC:header_size]
    new_file += write_u32(metadata_section_pos)
    new_file += file[header_size:file_size]

    # Write the section header
    new_file += write_u32(0x4D455441)  # signature
    new_file += write_u16(0x1)  # entry count
    new_file += write_u16(0x0)  # padding

    # Write the section entry
    current_size = 0
    new_file += write_bool(metadata.disable_oob_in_action)
    current_size += 1

    # Handle padding
    assert current_size <= STRUCT_SIZE
    while current_size != STRUCT_SIZE:
        new_file += write_u8(0x0)  # padding
        current_size += 1

    return new_file


def write_metadata(file, metadata: Metadata):
    new_file = file
    section_present = False
    for i in range(read_u16(file[0x8:0xA])):
        bound_start = i * 0x4 + 0x10
        bound_end = bound_start + 0x4
        offset = read_u32(file[bound_start:bound_end])

        file_pos = offset + read_u16(file[0xA:0xC])
        current_signature = read_u32(file[file_pos : file_pos + 4])

        if current_signature == 0x4D455441:
            print("INFO: Metadata section already present")
            return overwrite_old_metadata(file, metadata, file_pos)
    else:
        print("INFO: Metadata section not already present")
        return create_new_metadata(file, metadata)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("src_file", type=str)
    parser.add_argument("dst_file", type=str)
    args = parser.parse_args()

    with open(args.src_file, "rb") as f:
        file = f.read()

    if validate_file(file):
        new_file = write_metadata(file, read_config())

        # Revalidate the file to ensure we didn't destroy the KMP
        assert validate_file(new_file)

        with open(args.dst_file, "wb") as f:
            f.write(new_file)
