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
                    "4dbc7900b83b2253927450ce248ead97f9c49c57a6c99e43e881f7d100c4e783",
                    "7f6934ba7b3949d72da3c7701ca83c68")),
                Image("bl2.bin"),
                Image("pad.bin", stage=None),
                Image("u-boot.bin"),
                Image("el3_mon.bin", crypt=partial(crypt_file, el3_parts,
                    "b04bb88dd8a05e6f50cdd120607bda17897620aa751afa6a98e769d8756df1b0",
                    "1aa79845187ab8ca8c09e950f805c947")),
                Image("ssp.img"),
                Image("tail.bin", stage=None),
            )),
            Image("R7_EUR_OPEN.pit")
        )
    )
