# 0glabs-old-keys-restore

This script restores old `0G Labs` addresses from mnemonic phrases.

It supports two derivation schemes:

- old `validator` path: `m/44'/459'/0'/0/0`
- regular `storage / EVM` path: `m/44'/60'/0'/0/0`

For each mnemonic, it writes:

```text
validator: 0x...:0xprivatekey
Storage:0x...:0xprivatekey
```

The result is saved to `results.txt`.

## Requirements

- `Python 3.10+`
- `pip`

## Clone into a folder

### Windows PowerShell

```powershell
cd $HOME\Desktop
git clone https://github.com/VaniaHilkovets/0glabs-old-keys-restore.git
cd .\0glabs-old-keys-restore
```

### Linux

```bash
cd ~/Desktop
git clone https://github.com/VaniaHilkovets/0glabs-old-keys-restore.git
cd 0glabs-old-keys-restore
```

## Install dependencies

### Windows PowerShell

```powershell
pip install -r requirements.txt
```

### Linux

```bash
python3 -m pip install -r requirements.txt
```

## Prepare mnemonics

Open `seeds.txt` and put one mnemonic per line:

```text
word1 word2 word3 ... word24
word1 word2 word3 ... word24
```

Empty lines and lines starting with `#` are ignored.

## Run

### Windows PowerShell

```powershell
python 0g.py
```

### Linux

```bash
python3 0g.py
```

## What the script does

1. Reads mnemonic phrases from `seeds.txt`
2. Derives old `validator` and regular `storage` addresses
3. Saves everything to `results.txt`

Example output:

```text
validator: 0xBF75A9DAA7C8EA27F7371C27BFC7D48A8606E05E:0x...
Storage:0x0F668904aD4A52697452881D4886cb3c6a92e529:0x...
```

## Quick start

### Windows PowerShell

```powershell
cd $HOME\Desktop
git clone https://github.com/VaniaHilkovets/0glabs-old-keys-restore.git
cd .\0glabs-old-keys-restore
pip install -r requirements.txt
python 0g.py
```

### Linux

```bash
cd ~/Desktop
git clone https://github.com/VaniaHilkovets/0glabs-old-keys-restore.git
cd 0glabs-old-keys-restore
python3 -m pip install -r requirements.txt
python3 0g.py
```
