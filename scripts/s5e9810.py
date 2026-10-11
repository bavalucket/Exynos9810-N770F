from functools import partial
from decrypt import bl31_parts, cm_parts, crypt_file, el3_parts
from soc import SoC, Image

def soc_data():
    return SoC(
        signing_type=0,
        odin=(
            Image("cm.bin", crypt=partial(crypt_file, cm_parts,
                "4ad9af47e8ac6b21211e3068a91a0ec2c1b587a9e700743268467d328e03ad64",
                "4f395cde9defd4fa43e81996d794182e")),
            Image("keystorage.bin"),
            Image("sboot.bin", split=(
                Image("fwbl1.bin", stage="st1"),
                Image("bl31.bin", update_header=True, no_crc=True, crypt=partial(crypt_file, bl31_parts,
                    "821bbce30632a9dfa1c65e863961704a72e0e31cc78f0be0ce413919ff5db0bc",
                    "08fc06e11004efb540b85ddeeae65d69")),
                Image("bl2.bin"),
                Image("pad.bin", stage=None),
                Image("u-boot.bin"),
                Image("el3_mon.bin", crypt=partial(crypt_file, el3_parts,
                    "b04bb88dd8a05e6f50cdd120607bda17897620aa751afa6a98e769d8756df1b0",
                    "1bae98471d7ab9cc8c09fe50eb05ca40")),
                Image("ssp.img"),
                Image("tail.bin", stage=None),
            )),
            Image("R7_EUR_OPEN.pit")
        )
    )
