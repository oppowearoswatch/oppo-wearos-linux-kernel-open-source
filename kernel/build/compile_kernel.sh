#!/bin/bash
#======================================================================
#======================================================================
set -x
python -V
echo $@
echo $#
par_num=$#
par_list="$@"
TOP_DIR=`pwd`
echo "TOP_DIR=${TOP_DIR}"
export ANDROID_DIR=${TOP_DIR}/../android
export KERNEL_DIR=${TOP_DIR}
export PRODUCT=$1
export PATH=/usr/local/python2.7.7/bin:$PATH
python -V


usage(){
cat <<EOF

Usage: (mk) project actions [modules]

    usage: compile.sh <PROJECT> [new/new_user] 

    example:
        ./compile.sh MSM_XXX new
        ./compile.sh MSM_XXX new_user 
        ...
end

EOF
}

if [ x"$PRODUCT" = x"" ]; then
    usage
    exit 0
fi

function build_kernel()
{
    local return_val=0
    echo "enter kernel....."
    cd ${KERNEL_DIR}

    rm -rf ./out
    rm -rf compile_kernel.log

    if [ ${par_num} -gt 4 ];then
         echo "arg is too many"
         exit 1
    fi

    case ${PRODUCT#*_} in
        "19912") DEVICE=orca ;;
        "19908") DEVICE=beluga ;;
        *) echo Error: ${PRODUCT} is not supported!; exit 1
    esac

    if [ x"$2" = x"debug" ];then
         cp -r ${KERNEL_DIR}/private/msm-oppo-cw-extra/config/${DEVICE}_defconfig  ${KERNEL_DIR}/private/msm-oppo-cw-extra/config/msm8909w_defconfig
    elif [ x"$2" = x"user" ];then	
         cp -r ${KERNEL_DIR}/private/msm-oppo-cw-extra/config/${DEVICE}-perf_defconfig  ${KERNEL_DIR}/private/msm-oppo-cw-extra/config/msm8909w_defconfig
    fi
	
    ./build/build.sh 	2>&1 | tee -a  ${KERNEL_DIR}/compile_kernel.log
	
    tail -n 1 ${KERNEL_DIR}/compile_kernel.log | grep 'kernel_build_success'
    return_val=$?
    if [ ${return_val} -ne 0 ];then
        echo "============================build kernel error!!!==============================="
	exit 1
    fi
}

function copy_kernel_bin()
{
    echo "Start copy kernel bin for full build."

    if [ ${par_num} -gt 4 ];then
         echo "arg is too many"
         exit 1
    fi

    case ${PRODUCT#*_} in
        "19912") DEVICE=orca ;;
        "19908") DEVICE=beluga ;;
        *) echo Error: ${PRODUCT} is not supported!; exit 1
    esac
    if [ -f "${KERNEL_DIR}/out/android-msm-oppo-4.9/dist/zImage-dtb" ]; then 
       cp -f ${KERNEL_DIR}/out/android-msm-oppo-4.9/dist/*.ko  ${ANDROID_DIR}/device/oppo/${DEVICE}-kernel/
       cp -f ${KERNEL_DIR}/out/android-msm-oppo-4.9/dist/zImage-dtb  ${ANDROID_DIR}/device/oppo/${DEVICE}-kernel/kernel
    else
       exit 1
    fi	
    echo "end copy kernel bin for full build."
}
#=================================Main============================================
function main_start()
{
	#0、build_kernel
	export OPPO_NO_PREBUILD=true
	build_kernel $par_list
	copy_kernel_bin $par_list
}

main_start
