#Copyright (C) 2014 NXP Semiconductors, All Rights Reserved.
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License version 2 as
#published by the Free Software Foundation.

# make sure that the environment variables ARCH and CROSS_COMPILE
# are set for your architecture and cross compiler.
# And that KDIR points to the kernel to build against.
#
# e.g.:
# export ARCH=arm
# export CROSS_COMPILE=arm-linux-gnueabihf-
# export KDIR=../linux

EXTRA_CFLAGS += -DTFA98XX_GIT_VERSIONS=\"v6.6.2\"

EXTRA_CFLAGS += -I$(src)/inc
EXTRA_CFLAGS += -Werror

obj-y := snd-soc-tfa98xx.o

snd-soc-tfa98xx-objs += tfa98xx.o
snd-soc-tfa98xx-objs += tfa_container.o
snd-soc-tfa98xx-objs += tfa_dsp.o
snd-soc-tfa98xx-objs += tfa_init.o
