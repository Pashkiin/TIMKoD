import random

def read_file(file_name):
    with open(file_name, 'r') as f:
        return [f.read()]

def create_frequency_dict(text):
    frequency_dict = {}
    for char in text:
        frequency_dict[char] = frequency_dict.get(char, 0) + 1
    return dict(sorted(frequency_dict.items()))

def create_markov_list(text, order):
    markov_list = {}
    for i in range(len(text)-order):
        current_signs = text[i:i+order]
        next_sign = text[i+order]
        current_signs = current_signs + next_sign

        markov_list[current_signs] = markov_list.get(current_signs, 0) + 1
    return dict(sorted(markov_list.items()))

def generate_text(markov_list, initial_text, length, order):
    markov_list_items = list(markov_list.items())
    generated_text = initial_text

    for i in range(length):
        letter = generated_text[-len(initial_text):]

        filtered_markov_list_items = [item for item in markov_list_items if item[0].startswith(letter[-order:])]
        sum_markov_list = []
        sum_values = 0

        for item in filtered_markov_list_items:
            sum_values += item[1]
            sum_markov_list.append((item[0], sum_values))

        random_num = random.randint(0, sum_markov_list[-1][1])
        for item in sum_markov_list:
            if random_num <= item[1]:
                current_sign = item[0]
                break

        generated_text += current_sign[-1]

    return generated_text

def main():
    table = read_file('norm_hamlet.txt')
    #frequency_dict = create_frequency_dict(table[0])

    markov_list = create_markov_list(table[0], 1)
    markov_list_3rd = create_markov_list(table[0], 3)
    markov_list_5th = create_markov_list(table[0], 5)

    print("Test dla zrodla pierwszego rzedu: ", generate_text(markov_list, "t", 1000, 1))
    print("Test dla zrodla trzeciego rzedu: ", generate_text(markov_list_3rd, "To be", 1000, 3))
    print("Test dla zrodla piatego rzedu: ", generate_text(markov_list_5th, "Probability", 1000, 5))

if __name__ == "__main__":
    main()