
GLOW_HOME=~/devel/glow/build/Debug

for MODEL in model/*.onnx
do
    MODEL_BASE=`basename $MODEL .onnx`
    MODEL_DIR="./out/$MODEL_BASE"
    mkdir -p "$MODEL_DIR"
    $GLOW_HOME/bin/model-compiler \
        --model="$MODEL" \
        --emit-bundle="$MODEL_DIR" \
        --backend=CPU \
        --quantization-calibration=none \
        --quantization-precision=Int8 \
        --quantization-precision-bias=Int8 \
        --quantization-schema=symmetric \
        --bundle-api=static \
        --bundle-api-verbose \
        --relocation-model=pic \
        --optimize-ir \
        --dump-llvm-ir > "${MODEL_DIR}/${MODEL_BASE}.ll"
done
