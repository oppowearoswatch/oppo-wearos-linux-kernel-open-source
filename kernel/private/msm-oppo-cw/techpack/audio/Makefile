default: all

KBUILD_OPTIONS := AUDIO_ROOT=$(shell cd $(KERNEL_SRC); readlink -e $(M))
KBUILD_OPTIONS += MODNAME?=audio
KBUILD_OPTIONS += HEADER_INSTALL_DIR=$(KERNEL_SRC)/scripts
KBUILD_OPTIONS += UAPI_OUT=$(PWD)

TARGET_SUPPORT := apq8009

ifeq ($(TARGET_SUPPORT), $(filter $(TARGET_SUPPORT), sdm670 qcs605))
KBUILD_OPTIONS += CONFIG_ARCH_SDM670=y
endif
ifeq ($(TARGET_SUPPORT),sdm845)
KBUILD_OPTIONS += CONFIG_ARCH_SDM845=y
endif
ifeq ($(TARGET_SUPPORT),apq8053)
KBUILD_OPTIONS += CONFIG_ARCH_SDM450=y
endif
ifeq ($(TARGET_SUPPORT),apq8009)
KBUILD_OPTIONS += CONFIG_ARCH_MSM8909=y
endif

obj-m := ipc/
obj-m += dsp/
obj-m += dsp/codecs/
obj-m += soc/
obj-m += asoc/
obj-m += asoc/codecs/
obj-m += asoc/codecs/tfa98xx/

ifeq ($(TARGET_SUPPORT), $(filter $(TARGET_SUPPORT), sdm670 qcs605))
obj-m += asoc/codecs/wcd934x/
endif
ifeq ($(TARGET_SUPPORT), $(filter $(TARGET_SUPPORT), apq8053 sdm670 qcs605 apq8009))
obj-m += asoc/codecs/sdm660_cdc/
endif
ifeq ($(TARGET_SUPPORT), $(filter $(TARGET_SUPPORT), sdm670 qcs605))
obj-m += asoc/codecs/msm_sdw/
endif



all:
	$(shell rm -fr $(shell pwd)/soc/core.h)
	$(shell ln -s $(KERNEL_SRC)/drivers/pinctrl/core.h $(shell pwd)/soc/core.h)
	$(shell rm -fr $(shell pwd)/include/soc/internal.h)
	$(shell ln -s $(KERNEL_SRC)/drivers/base/regmap/internal.h $(shell pwd)/include/soc/internal.h)
	$(shell rm -fr $(shell pwd)/soc/pinctrl-utils.h)
	$(shell ln -s $(KERNEL_SRC)/drivers/pinctrl/pinctrl-utils.h $(shell pwd)/soc/pinctrl-utils.h)
	$(MAKE) -C $(KERNEL_SRC) M=$(M) modules $(KBUILD_OPTIONS)

modules_install:
	$(MAKE) INSTALL_MOD_STRIP=1 M=$(M) -C $(KERNEL_SRC) modules_install

clean::
	rm -f *.o *.ko *.mod.c *.mod.o *~ .*.cmd Module.symvers
	rm -rf .tmp_versions
