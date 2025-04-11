import numpy as np
import random


def get_input():
    while True:
        binary_string = input("Introduceti un sir binar (multiplu de 7): ")
        if all(c in '01' for c in binary_string) and len(binary_string) % 7 == 0:
            return binary_string
        print("Sirul trebuie sa fie format din 0 si 1 si sa aiba o lungime multiplu de 7.")


def create_matrix(binary_string):
    rows = len(binary_string) // 7
    matrix = np.array(list(binary_string), dtype=int).reshape(rows, 7)
    return matrix


def calculate_parity(matrix):
    rows, cols = matrix.shape
    parity_matrix = np.zeros((rows + 1, cols + 1), dtype=int)
    parity_matrix[:-1, :-1] = matrix

    for i in range(rows):
        parity_matrix[i, -1] = np.sum(matrix[i, :]) % 2
    for j in range(cols):
        parity_matrix[-1, j] = np.sum(parity_matrix[:-1, j]) % 2

    parity_matrix[-1, -1] = np.sum(parity_matrix[-1, :-1]) % 2
    return parity_matrix


def introduce_error(matrix):
    rows, cols = matrix.shape
    error_row = random.randint(0, rows - 2)
    error_col = random.randint(0, cols - 2)
    matrix[error_row, error_col] ^= 1
    return error_row, error_col


def detect_error(matrix):
    recalculated = calculate_parity(matrix[:-1, :-1])
    error_positions = np.argwhere(recalculated != matrix)
    if error_positions.size > 0:
        return tuple(error_positions[0])
    return None


def display_matrix(matrix):
    rows, cols = matrix.shape
    for i in range(rows - 1):
        print("".join(map(str, matrix[i, :-1])) + " | " + str(matrix[i, -1]))
    print("-" * (cols * 2))
    print("".join(map(str, matrix[-1, :-1])) + " | " + str(matrix[-1, -1]))


def crc_division(dividend, divisor):
    dividend = list(dividend.lstrip('0'))
    divisor_len = len(divisor)
    steps = [("".join(dividend), divisor)]

    while len(dividend) >= divisor_len:
        for i in range(divisor_len):
            dividend[i] = str(int(dividend[i]) ^ int(divisor[i]))

        while dividend and dividend[0] == '0':
            dividend.pop(0)

        steps.append(("".join(dividend) if dividend else '0', divisor))

    remainder = "".join(dividend) if dividend else '0'

    return remainder, steps


def crc(final=None):
    data = input("Introduceti mesajul binar (M(x)): ")
    generator = input("Introduceti polinomul generator binar (C(x)): ")

    while generator and generator[0] == '0':
        generator.pop(0)

    if not (all(c in '01' for c in data) and all(c in '01' for c in generator)):
        print("Datele trebuie să fie binare!")
        return

    if len(data) < len(generator):
        print("Lungimea mesajului trebuie să fie mai mare decât lungimea polinomului generator!")
        return

    extended_data = data + '0' * (len(generator) - 1)
    print(f"\nMesajul extins (T(x)): {extended_data}")
    print(f"Polinomul generator (C(x)): {generator}")
    print("\nEfectuăm împărțirea CRC:\n")

    remainder, steps = crc_division(extended_data, generator)

    for step in steps[:-1]:
        print(step[0])
        print(step[1])
        print("-" * len(step[0]))
    print(steps[-1][0])

    transmitted_message = data + remainder
    print(f"\nMesaj transmis (M'(x)): {transmitted_message}")
    print(f"Rest CRC (R(x)): {remainder}")

    check, _ = crc_division(transmitted_message, generator)

    if all(c == '0' for c in check):
        print("\nProba: Restul este 0 -> Fără erori!")
    else:
        print("\nProba: Restul este diferit de 0 -> Cu erori!")

    check = check.zfill(len(extended_data))
    final = "".join(str(int(extended_data[i]) ^ int(check[i])) for i in range(len(extended_data)))

    print(f"\nMesaj final după XOR cu restul: {final}")

def menu():
    while True:
        print("\nMeniu:")
        print("1. Verificare Paritate Bidimensionala")
        print("2. Verificare CRC")
        print("3. Iesire")
        choice = input("Optiunea: ")
        if choice == '1':
            binary_string = get_input()
            original_matrix = create_matrix(binary_string)
            parity_matrix = calculate_parity(original_matrix)
            print("\nMatricea cu biti de paritate:")
            display_matrix(parity_matrix)

            transmitted_message = "".join(map(str, parity_matrix[:-1, :].flatten()))
            print("\nMesaj transmis =", transmitted_message)

            error_row, error_col = introduce_error(parity_matrix)
            print(f"\nBit corupt la ({error_row}, {error_col})")
            print("\nMatricea corupta:")
            display_matrix(parity_matrix)

            detected_error = detect_error(parity_matrix)
            if detected_error:
                print(f"\nEroare detectata la pozitia: {detected_error}")
            else:
                print("\nNu s-au detectat erori.")
        elif choice == '2':
            crc()
        elif choice == '3':
            break
        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    menu()