default: all

KBUILD_OPTIONS := WLAN_ROOT=$(shell cd $(KERNEL_SRC); readlink -e $(M))


WLAN_CHIPSET := pronto
WLAN_SELECT := CONFIG_PRONTO_WLAN=m

KBUILD_OPTIONS += MODNAME?=wlan
KBUILD_OPTIONS += BOARD_PLATFORM=msm8909
KBUILD_OPTIONS += $(WLAN_SELECT)

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(M) modules $(KBUILD_OPTIONS)

modules_install:
	$(MAKE) INSTALL_MOD_STRIP=1 M=$(M) -C $(KERNEL_SRC) modules_install

clean::
	rm -f *.o *.ko *.mod.c *.mod.o *~ .*.cmd Module.symvers
	rm -rf .tmp_versions
