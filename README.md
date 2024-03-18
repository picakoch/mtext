# Dataset generation

Use `mtext_gen_dataset.py` to generate a proper Huggingface dataset object from raw file.

# Fine-tune model

Config files for axotlotl (https://github.com/OpenAccess-AI-Collective/axolotl) are provided for Llama2 and Mistral fine-tuning.

# Training on VAST.AI

Create an instance based on the following docker image:

`winglian/axolotl:main-py3.10-cu118-2.1.2`

Choose a machine xith 2xRTX 4090.

Start the VM.

Copy config file from your machine to the VM:

```scp -P <PORT> <CONFIG>.yml root@ssh8.vast.ai:/root/axolotl/configs/```

Connect ot the VM and run

```
cd /root/axolotl/
huggingface-cli login --token <HF_TOKEN>
wandb login <WANDBD_TOKEN>
accelerate launch -m axolotl.cli.train configs/<CONFIG>.yml
```

One training is finished, merge weights:

```
python3 -m axolotl.cli.merge_lora configs/<CONFIG>.yml
huggingface-cli upload <HF_REPO> out/merged/ .
```