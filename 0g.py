from hashlib import new as hashlib_new, sha256
from pathlib import Path

from eth_account import Account
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


Account.enable_unaudited_hdwallet_features()

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
PROFILES = [
    ("validator_old", 459),
    ("storage_or_eth", 60),
]
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "seeds.txt"
OUTPUT_FILE = BASE_DIR / "results.txt"


def bech32_polymod(values):
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    checksum = 1
    for value in values:
        top = checksum >> 25
        checksum = ((checksum & 0x1FFFFFF) << 5) ^ value
        for i in range(5):
            if (top >> i) & 1:
                checksum ^= generator[i]
    return checksum


def bech32_hrp_expand(hrp):
    return [ord(char) >> 5 for char in hrp] + [0] + [ord(char) & 31 for char in hrp]


def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join(CHARSET[d] for d in combined)


def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    result = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1

    for value in data:
        if value < 0 or (value >> frombits):
            raise ValueError("Invalid value for convertbits")
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            result.append((acc >> bits) & maxv)

    if pad:
        if bits:
            result.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise ValueError("Invalid padding in convertbits")

    return result


def evm_to_0g(evm_address):
    address_bytes = bytes.fromhex(evm_address.removeprefix("0x"))
    data = convertbits(address_bytes, 8, 5)
    return bech32_encode("0g", data)


def cosmos_hex_from_private_key(private_key_bytes):
    private_key_int = int.from_bytes(private_key_bytes, "big")
    private_key = ec.derive_private_key(private_key_int, ec.SECP256K1())
    compressed_pubkey = private_key.public_key().public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.CompressedPoint,
    )
    return "0x" + hashlib_new("ripemd160", sha256(compressed_pubkey).digest()).digest().hex()


def derive_profile(mnemonic, coin_type, account=0, change=0, index=0):
    path = f"m/44'/{coin_type}'/{account}'/{change}/{index}"
    wallet = Account.from_mnemonic(mnemonic, account_path=path)
    private_key = "0x" + bytes(wallet.key).hex()
    evm_address = wallet.address
    wallet_0g = evm_to_0g(evm_address)
    cosmos_hex = cosmos_hex_from_private_key(bytes(wallet.key))
    return {
        "path": path,
        "wallet_0g": wallet_0g,
        "evm_address": evm_address,
        "private_key": private_key,
        "cosmos_hex": cosmos_hex,
    }


def load_mnemonics(path):
    mnemonics = []
    with open(path, "r", encoding="utf-8") as infile:
        for raw_line in infile:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            mnemonics.append(line)
    return mnemonics


def build_report(mnemonics, account=0, change=0, index=0):
    sections = []
    for mnemonic in mnemonics:
        validator = derive_profile(
            mnemonic,
            coin_type=459,
            account=account,
            change=change,
            index=index,
        )
        storage = derive_profile(
            mnemonic,
            coin_type=60,
            account=account,
            change=change,
            index=index,
        )
        lines = [
            f"validator: {validator['evm_address']}:{validator['private_key']}",
            f"Storage:{storage['evm_address']}:{storage['private_key']}",
        ]
        sections.append("\n".join(lines))
    return "\n\n".join(sections) + ("\n" if sections else "")


def main():
    mnemonics = load_mnemonics(INPUT_FILE)
    report = build_report(mnemonics)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as outfile:
        outfile.write(report)

    print(f"Processed {len(mnemonics)} mnemonic(s).")
    print(f"Read from: {INPUT_FILE}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
