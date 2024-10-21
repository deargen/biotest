# 복잡한 프로젝트 configuration 명확하게 하기

Configuration은 일반적으로 다음과 같은 방식이 널리 사용됩니다.

1. argparse
2. yaml

그러나, **두 방법 모두 단점**이 있으며 해당 문서에서는 단점과 개인적인 workflow를 해결책으로써 제시합니다.


## TL;DR

[dataclass 솔루션](#dataclass)

## 좋은 config 시스템

Configuration style은 프로젝트마다 다르고 방식은 다양합니다. 하지만 빠르게 다양한 hyperparameter로 실험을 해봐야 하는 연구 코드에서 좋은 configuration 시스템은 다음과 같다고 생각합니다. (필자의 정의)

1. typing과 default 값을 쉽게 추적이 가능함
2. 사용법과 parameter 종류, 값 등이 예측하기 쉬워야 함.
3. 복잡한 dependency가 있는것 보단 간단명료해서 maintain하기 쉬워야 함.

## 나쁜 config 시스템

1. 변수들이 읽어들이는 파일에 따라 dynamic하게 생성되어 코드를 보며 따라가기 너무 힘들고 실행을 해봐야 알 수 있는 경우.
2. 너무 심하게 generalisation을 하려고 해서, 실행하려는 툴(`train.py`, `eval.py` 등)에 따라 필요한 파라메터가 다른데도 불구하고 사용되지 않는것이 너무 많이 포함 돼 알기 어려운 경우.
3. 모든 파일이 config 시스템과 연동되어있어 다른 파일/프로젝트에서 일부 모듈만 쉽게 가져다 쓰기 어려운 경우.

### 나쁜 예시 (argparse 후 sanitise 하는 방식)

[kohya_ss/library/config_util.py](https://github.com/bmaltais/kohya_ss/blob/f8d2673641778ed5b362f107f9f92a20aa15979a/library/config_util.py#L651-L687)

main을 보면, 몇 가지 parameter를 argparse에 넣으면 그에 맞게 config sanitisation 등을 하고 그 결과를 바탕으로 또 한번 processing을 해서 BlueprintGenerator라는 이상한걸 만듦.

1. ConfigSanitizer와 BlueprintGenerator가 너무 추상적이고 dynamic해서 어떤 값이 나올지 실행 전에는 전혀 예상이 안됨. (코드 읽어보기)
    - 코드에서 없는 변수를 써서 오류가 날 수 있음.
    - 변수의 type이나 값이 어떻게 생겼는지 알 수가 없음.
    - 만약 예상되는 값들이 있다고 해도, 그 값의 default가 무엇인지 쉽게 Pylance로 찾기 힘듦. 해당 default가 정의된 파일을 찾아가야함.
2. 너무 많은 값을 command line에 넣어야 해서 쉘 스크립트가 복잡해짐.
    ```sh
    # 안 좋은 예시
    python train_dreambooth.py \
        --pretrained_model_name_or_path=$MODEL_NAME  \
        --instance_data_dir=$INSTANCE_DIR \
        --class_data_dir=$CLASS_DIR \
        --output_dir=$OUTPUT_DIR \
        --with_prior_preservation --prior_loss_weight=1.0 \
        --instance_prompt="a photo of sks dog" \
        --class_prompt="a photo of dog" \
        --resolution=512 \
        --train_batch_size=1 \
        --gradient_accumulation_steps=1 --gradient_checkpointing \
        --use_8bit_adam \
        --enable_xformers_memory_efficient_attention \
        --set_grads_to_none \
        --learning_rate=2e-6 \
        --lr_scheduler="constant" \
        --lr_warmup_steps=0 \
        --num_class_images=200 \
        --max_train_steps=800 \
        --push_to_hub
    ```
3. 중간의 command-line argument를 지우면 프로그램이 동작하지 않거나 이후 argument들이 무시되는 경우가 있음.

### 나쁜 예시 2 (yaml 방식)

[SlowFast/slowfast/datasets/imagenet.py](https://github.com/facebookresearch/SlowFast/blob/2efb99faa254075b4e28d3d4f313052b51da05bc/slowfast/datasets/imagenet.py#L180)

[SlowFast/configs/AVA/SLOWFAST_32x2_R50_SHORT.yaml](https://github.com/facebookresearch/SlowFast/blob/2efb99faa254075b4e28d3d4f313052b51da05bc/configs/AVA/SLOWFAST_32x2_R50_SHORT.yaml#L46)

1. hard-coding 된 값이 많아서 어떻게 사용하는건지 이해하기 어려움 (긴 리스트가 있는데 무슨 값을 의미하는지?)
2. 값들이 dependency가 많아서 제대로 이해하지 않으면 오류나기 쉬움 (예: LOCATION, GROUP, POOL은 list 길이가 같아야 함.)

## 저 만의 솔루션 (dataclass)

사용법을 먼저 보여드리자면, 

### ::: ml_project.utils.config.ExampleConfig
    options:
        show_docstring_description: true
        show_docstring_examples: false
        members: false
        show_bases: false
        show_source: true

### ::: ml_project.utils.config.ExampleConfig
    options:
        show_docstring_description: false
        show_docstring_examples: true
        members: false
        show_bases: false
        show_source: false

BaseConfig 소스코드:  
### ::: ml_project.utils.config.BaseConfig
    options:
        show_docstring_description: false
        show_docstring_examples: false
        members: false
        show_bases: false
        show_source: true

### 장점

1. 간단 명료한 dataclass를 만들어 typing 및 default 값 pylance의 go to definition 기능으로 확인하기 좋음.
2. 변경하고자 하는 변수들은 환경변수를 이용해 변경 가능.
3. 변경된 변수들은 따로 print 해놓아서, 정말 실험에 중요한 점이 무엇인지 쉽게 확인 가능.
    - 만약 100개의 parameter가 그냥 출력된다면 어떤 목적으로 실험을 돌린것인지 확인하기 어려움.
4. 추가 기능은 method 더 만들어 `__post_init__`에 넣으면 됨. 확장이 편리.
5. 없는 변수를 수정하고자 한 경우 에러 발생해 오타 등 실수 방지.
6. 쉘 스크립트 작성이 간편해짐. 특히 많은 parameter 변동이 있을 때 컨트롤이 빠름.
    ```sh
    # 좋은 예시
    for batch_size in {1..3}; do
        export MLCONFIG_batch_size=$batch_size
        for lr in {1..3}; do
            export MLCONFIG_lr=$lr
            for iter in {1..3}; do
                export MLCONFIG_iter=$iter
                python train.py  # argparse처럼 command가 복잡해지지 않음.
            done
        done
    done
    ```

## typer를 이용한 방법

Typer는 argparse보다 장점이 많습니다.

1. typing을 이용해 명확하게 parameter를 정의할 수 있음.
2. command line 프로그램이 쉽게 API로 노출됨.
    - 예: `my-program run --batch-size 32` 를 `import my_program; my_program.run(batch_size=32)`로 사용 가능
3. shell completion도 쉽게 설치해 사용 가능.

복잡한 config 대신 typer를 이용해 command line argument로 사용하는 것도 좋은 방법입니다. 특히 다음과 같은 경우에 유용합니다.

1. 변수 개수가 몇 개 없는 경우

