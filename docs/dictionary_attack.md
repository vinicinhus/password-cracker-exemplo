# Dictionary Attack

## Descrição

O ataque de dicionário é uma técnica de criptografia onde uma lista predefinida de possíveis senhas (wordlist) é usada
para tentar descobrir a senha correta. Este método é mais eficiente do que a força bruta, pois se baseia em senhas
comuns e palavras conhecidas.

## Código

O código `dictionary_attack.py` implementa um ataque de dicionário para tentar descobrir uma senha hash. Abaixo está uma
explicação detalhada do código:

```python
from multiprocessing import Pool, cpu_count
from hash_functions import verify_password_bcrypt, hash_password_bcrypt
import time


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
```

## Explicação

1. **Importação de Módulos:**
    - Importa módulos necessários como `multiprocessing.Pool`, `time` e funções de hash.

2. **Função `generate_example_hash`:**
    - Gera um hash para a senha "qwerty" usando `hash_password_bcrypt`.

3. **Função `attempt_password`:**
    - Tenta verificar uma senha candidata contra o hash fornecido. Retorna a senha se for correta.

4. **Função `dictionary_attack`:**
    - Lê uma lista de senhas de um arquivo de wordlist.
    - Utiliza múltiplos processos para tentar todas as senhas da wordlist contra o hash fornecido até encontrar a
      correta.

5. **`if __name__ == "__main__"`:**
    - Gera um hash de exemplo, mede o tempo de execução do ataque de dicionário e imprime a senha encontrada e o tempo
      total gasto.
