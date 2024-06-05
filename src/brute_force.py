import itertools
import string
import time
from multiprocessing import Pool, cpu_count, Value

from hash_functions import verify_password_bcrypt, hash_password_bcrypt

# Variável compartilhada para indicar se uma senha foi encontrada
password_found = Value("i", 0)


def generate_example_hash():
    password = "ab"
    hashed = hash_password_bcrypt(password)
    return hashed


def attempt_password(args):
    guess, hashed_password = args

    print(f"Tentando senha: {guess}")  # Printando cada tentativa de senha
    try:
        if verify_password_bcrypt(guess, hashed_password):
            with password_found.get_lock():
                if password_found.value == 0:
                    password_found.value = 1
                    return guess
    except ValueError as e:
        print(f"Erro ao verificar senha: {e}")
    return None


def generate_passwords(length, chars):
    return ("".join(guess) for guess in itertools.product(chars, repeat=length))


def brute_force_crack(hashed_password):
    chars = string.ascii_letters + string.digits
    pool = Pool(cpu_count())
    for length in range(1, 6):  # Tentando senhas de 1 a 5 caracteres
        passwords = generate_passwords(length, chars)
        for result in pool.imap_unordered(
                attempt_password, ((pw, hashed_password) for pw in passwords)
        ):
            if result is not None:
                pool.terminate()
                return result
    return None


if __name__ == "__main__":
    hashed_password = generate_example_hash()
    print(f"Hashed password: {hashed_password}")

    start_time = time.time()
    cracked_password = brute_force_crack(hashed_password)
    end_time = time.time()

    if cracked_password:
        print(f"Senha encontrada: {cracked_password}")
    else:
        print("Senha não encontrada.")

    print(f"Tempo total: {end_time - start_time:.2f} segundos")
