# 0glabs-old-keys-restore

Скрипт для восстановления старых `0G Labs` адресов из сид-фраз.

Поддерживает 2 схемы:

- старый `validator` путь: `m/44'/459'/0'/0/0`
- обычный `storage / EVM` путь: `m/44'/60'/0'/0/0`

На выходе для каждой сид-фразы пишет:

```text
validator: 0x...:0xprivatekey
Storage:0x...:0xprivatekey
```

Результат сохраняется в `results.txt`.

## Что нужно

- `Python 3.10+`
- `pip`

## Как скачать в папку

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

## Установка зависимостей

### Windows PowerShell

```powershell
pip install -r requirements.txt
```

### Linux

```bash
python3 -m pip install -r requirements.txt
```

## Права на запуск

### Windows

На Windows ничего выдавать не нужно.

### Linux

Если хотите запускать как исполняемый файл:

```bash
chmod +x 0g.py
```

Но обычно достаточно просто:

```bash
python3 0g.py
```

## Как подготовить сид-фразы

Откройте файл `seeds.txt` и вставьте сид-фразы по одной на строку:

```text
word1 word2 word3 ... word24
word1 word2 word3 ... word24
```

Пустые строки и строки с `#` игнорируются.

## Запуск

### Windows PowerShell

```powershell
python 0g.py
```

### Linux

```bash
python3 0g.py
```

## Что будет после запуска

Скрипт:

1. читает сид-фразы из `seeds.txt`
2. считает `validator` и `storage` адреса
3. сохраняет результат в `results.txt`

Пример вывода:

```text
validator: 0xBF75A9DAA7C8EA27F7371C27BFC7D48A8606E05E:0x...
Storage:0x0F668904aD4A52697452881D4886cb3c6a92e529:0x...
```

## Быстрый старт

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
