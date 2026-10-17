from soc import SoC, Image

def soc_data():
    return SoC(
        signing_type=0,
        odin=(
            Image("cm.bin", no_crc=True),
            Image("sboot.bin", no_crc=True, split=(
                Image("fwbl1.bin", stage="st1"),
                Image("bl31.bin", update_header=True, no_crc=True),
                Image("bl2.bin", no_crc=True),
                Image("pad.bin", stage=None),
                Image("u-boot.bin", no_crc=True),
                Image("ssp.img", no_crc=True),
                Image("tail.bin", stage=None),
            )),
            Image("modem.bin", no_crc=True, split=(
                Image("TOC.bin", stage=None),
                Image("BOOT.bin", no_crc=True),
                Image("pad.bin", stage=None),
                Image("MAIN.bin", no_crc=True),
                Image("tail.bin", stage=None),
            )),
            Image("HERO2LTE_EUR_OPEN_HIDDEN45M.pit", no_crc=True)
        )
    )
