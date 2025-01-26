import timeit

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

encodings = ['Windows-1251', 'utf-8', 'cp1251', 'iso-8859-1']

for enc in encodings:
    try:
        with open("st1.txt", "r", encoding=enc) as file:
            text1 = file.read()
        print(f"Файл 'st1.txt' успішно прочитано з кодуванням {enc}")
        break
    except UnicodeDecodeError:
        print(f"Помилка при читанні 'st1.txt' з кодуванням {enc}")

for enc in encodings:
    try:
        with open("st2.txt", "r", encoding=enc) as file:
            text2 = file.read()
        print(f"Файл 'st2.txt' успішно прочитано з кодуванням {enc}")
        break
    except UnicodeDecodeError:
        print(f"Помилка при читанні 'st2.txt' з кодуванням {enc}")

existing_pattern = "методи"
non_existing_pattern = "ПтнХу*ло"

def measure_time(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=1000)

bm_time1_existing = measure_time(boyer_moore_search, text1, existing_pattern)
kmp_time1_existing = measure_time(kmp_search, text1, existing_pattern)
rk_time1_existing = measure_time(rabin_karp_search, text1, existing_pattern)

bm_time1_non_existing = measure_time(boyer_moore_search, text1, non_existing_pattern)
kmp_time1_non_existing = measure_time(kmp_search, text1, non_existing_pattern)
rk_time1_non_existing = measure_time(rabin_karp_search, text1, non_existing_pattern)

bm_time2_existing = measure_time(boyer_moore_search, text2, existing_pattern)
kmp_time2_existing = measure_time(kmp_search, text2, existing_pattern)
rk_time2_existing = measure_time(rabin_karp_search, text2, existing_pattern)

bm_time2_non_existing = measure_time(boyer_moore_search, text2, non_existing_pattern)
kmp_time2_non_existing = measure_time(kmp_search, text2, non_existing_pattern)
rk_time2_non_existing = measure_time(rabin_karp_search, text2, non_existing_pattern)

print("Стаття 1:")
print(f"Боєра-Мура (існуючий підрядок): {bm_time1_existing}")
print(f"Кнута-Морріса-Пратта (існуючий підрядок): {kmp_time1_existing}")
print(f"Рабіна-Карпа (існуючий підрядок): {rk_time1_existing}")
print(f"Боєра-Мура (вигаданий підрядок): {bm_time1_non_existing}")
print(f"Кнута-Морріса-Пратта (вигаданий підрядок): {kmp_time1_non_existing}")
print(f"Рабіна-Карпа (вигаданий підрядок): {rk_time1_non_existing}")

print("\nСтаття 2:")
print(f"Боєра-Мура (існуючий підрядок): {bm_time2_existing}")
print(f"Кнута-Морріса-Пратта (існуючий підрядок): {kmp_time2_existing}")
print(f"Рабіна-Карпа (існущий підрядок): {rk_time2_existing}")
print(f"Боєра-Мура (вигаданий підрядок): {bm_time2_non_existing}")
print(f"Кнута-Морріса-Пратта (вигаданий підрядок): {kmp_time2_non_existing}")
print(f"Рабіна-Карпа (вигаданий підрядок): {rk_time2_non_existing}")

'''
St1:
Алгоритм Боєра-Мура показав найкращі результати як для існуючого, так і для вигаданого підрядка.
Це пов'язано з тим, що він ефективно пропускає непотрібні порівняння за допомогою таблиці зсувів, 
що особливо корисно для довгих текстів.
St2:
Алгоритм Боєра-Мура також виявився найшвидшим як для існуючого, 
так і для вигаданого підрядка. Це підтверджує його ефективність для текстів різного обсягу.

Алгоритм Кнута-Морріса-Пратта показав гірші результати порівняно з Боєра-Мура, але все ще кращі, ніж Рабіна-Карпа.
Алгоритм Рабіна-Карпа виявився найповільнішим для обох текстів, особливо для вигаданого підрядка.
'''