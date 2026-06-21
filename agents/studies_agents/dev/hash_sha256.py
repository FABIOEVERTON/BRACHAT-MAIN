import hashlib


def calc_hash(word: str) -> str:
    return hashlib.sha256(word.encode("utf-8")).hexdigest()


def main():
    word = "BRACHÁT"
    result = calc_hash(word)
    print(result)


if __name__ == "__main__":
    main()
