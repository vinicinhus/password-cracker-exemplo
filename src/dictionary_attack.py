import time
from multiprocessing import Pool, cpu_count

from hash_functions import verify_password_bcrypt, hash_password_bcrypt


def generate_example_hash():
    password = "qwerty"
    hashed = hash_password_bcrypt(password)
    return hashed


def attempt_password(args):
    password, hashed_password = args
    try:
        if verify_password_bcrypt(password, hashed_password):
            return password
    except ValueError as e:
        print(f"Erro ao verificar senha: {e}")
    return None


def dictionary_attack(hashed_password, wordlist):
    with open(wordlist, "r") as file:
        passwords = [line.strip() for line in file]

    pool = Pool(cpu_count())
    for result in pool.imap_unordered(
            attempt_password, ((pw, hashed_password) for pw in passwords)
    ):
        if result is not None:
            pool.terminate()
            return result
    return None


if __name__ == "__main__":
    # Gerar um hash de exemplo para uma senha conhecida
    hashed_password = generate_example_hash()
    print(f"Hashed password: {hashed_password}")

    wordlist = "src/wordlist.txt"

    start_time = time.time()
    cracked_password = dictionary_attack(hashed_password, wordlist)
    end_time = time.time()

    if cracked_password:
        print(f"Senha encontrada: {cracked_password}")
    else:
        print("Senha não encontrada.")

    print(f"Tempo total: {end_time - start_time:.2f} segundos")
