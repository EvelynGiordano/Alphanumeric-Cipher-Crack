from collections import Counter
import re
import sys

alphabet = {
        "A": None, "B": None,
        "C": None, "D": None,
        "E": None, "F": None,
        "G": None, "H": None,
        "I": None, "J": None,
        "K": None, "L": None,
        "M": None, "N": None,
        "O": None, "P": None,
        "Q": None, "R": None,
        "S": None, "T": None,
        "U": None, "V": None,
        "W": None, "X": None,
        "Y": None, "Z": None,
    }

process = [
            "the",
            "to",
            "who",
            "that",
            "are", # ape, ale, age, ace, awe, axe (all unlikely)
            "and",
            "for",
            "been",
            "but",
            "know",
            "put",
            "have",
            "would",
            "could",
            "should",
            "and",
            "was",
            "why"

        ]

found = []

# region Norvig's Spell Checker

# The following is Peter Norvig's Bayesian Spellchecker written in 2007
# Uses Bayesian modeling to get the probability that a mistyped word is a candidate word
# Candidate words are words that are one- to two- letter edits away from the mistyped words
# The candidate word with the highest probability of being the mistyped word is returned
# https://norvig.com/spell-correct.html

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# endregion

def most_common_words(t):
    with open(t) as fin:
        counter = Counter(fin.read().strip().split())

    return counter.most_common()


def most_common_letters(t):
    with open(t, encoding="utf8") as f:
        c = Counter()
        for line in f:
            alphanumeric_filter = filter(str.isalnum, line)
            alphanumeric_string = "".join(alphanumeric_filter)
            c += Counter(str(alphanumeric_string).upper())

    return c.most_common()


def get_pattern(s):
    i = 0
    pattern = []
    letters = {}
    for c in s:
        if c in letters:
            pattern.append(letters[c])
        else:
            pattern.append(i)
            letters.update({c: i})
        i = i+1

    return pattern


def replace_text(t, c, oc):
    with open(t, 'r', encoding="utf8") as file:
        data = file.read()
    data = data.replace(oc, c)
    with open("replaced", 'w', encoding="utf8") as file:
        file.write(data)



def equal_lower_cases(word, encrypted_word):
    i = 0
    if(len(word) != len(encrypted_word)):
        return False
    for x in encrypted_word:
        if str(x).isupper():
            i = i+1
            continue
        elif x == word[i]:
            i = i+1
            continue
        else:
            return False
    return True


def replace_uppercase(word, encrypted_word):
        i = 0
        for x in encrypted_word:
            if str(x).isupper():
                    # replace character in 'replaced.txt'
                    replace_text("replaced", word[i], x)
                    # set character in the dictionary
                    alphabet[str(word[i]).upper()] = x
                    found.insert(0, str(word[i]).upper())
                    i=i+1
            else:
                i=i+1

# returns True if there are too many uppercase letters in the given word
# returns False if there is only one uppercase letter in the given word, and also when dealing with "the" (base case)
def num_encrypted_letters(x, w):
    if len(x) == 1:
        return False
    elif w == "the":
        return False
    else:
        encrypted_letters = 0
        for i in x:
            if str(i).isupper():
                encrypted_letters = encrypted_letters + 1
        if encrypted_letters > 1:
            return True
        else:
            return False


def percentage_key():
    total = 0
    i = 0
    key = "AZERTYUIOPQSDFGHJKLMWXCVBN"

    wanted_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']  # The keys you want
    final = dict((k, alphabet[k]) for k in wanted_keys if k in alphabet)

    for val in final:
        if final[val] == key[i]:
            total = total + 1
        i = i + 1

    return print("PERCENTAGE OF KEY DECRYPTED: ", total/26 * 100, "%")

def contains_upper(t):
    with open(t, encoding="utf8") as f:
        for line in f:
            if any(letter.isupper() for letter in line):
                return True
    return False

def run_process(list):
    for w in list:
        common_encrypted_words = most_common_words("replaced")
        for e in common_encrypted_words:
            e = e[0]
            if num_encrypted_letters(e, w) or not equal_lower_cases(w,e):
                continue
            else:
                if get_pattern(w) == get_pattern(e):
                        replace_uppercase(w, e)
                        break
                else:
                    continue

def run_spell_checker(list_of_words):
    done = False
    if contains_upper("replaced"):
        for i in list_of_words:
            i = i[0]
            c = correction(i)
            if str(i).islower() or  i == correction(i) or len(i) < 3 or not equal_lower_cases(correction(i), i) or num_encrypted_letters(i, ""):
                continue
            else:
                j = 0
                for x in i:
                    if str(x).isupper() and not already_done(str(c[j]).upper()):
                            replace_uppercase(c, i)
                            done = True
                            break
                    else:
                        j = j+1
                        continue
            if done:
                run_spell_checker(most_common_words("replaced"))
                break

def already_done(key):
    res = False
    if alphabet.get(key):
        res = True

    return res

# test key: AZERTYUIOPQSDFGHJKLMWXCVBN
def hack_cipher(t):
    common_encrypted_letters = most_common_letters(t)
    alphabet["E"] = common_encrypted_letters[0][0]
    replace_text(t, 'e', alphabet["E"])

    run_process(process)
    run_spell_checker(most_common_words("replaced"))

    unfound = 0
    for x in alphabet.values():
        if x == None:
            unfound = unfound + 1

    if unfound == 1:
        a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for x in alphabet:
            if alphabet[x] != None:
                a = a.replace(alphabet[x], "")
            else:
                k = x
        alphabet[k] = a


    with open("key.txt", "w", encoding="utf8") as final:
        for x in alphabet.values():
            if x == None:
                final.write("_")
            else:
                final.write(x)

    with open("key.txt", "r", encoding="utf8") as final:
            print(final.read())


def main():
    file = sys.argv[1]

    with open(file, 'r', encoding="utf8") as inp:
        y = inp.read().upper()

    with open("capitalized", 'w', encoding="utf8") as out:
        out.write(y)

    with open("capitalized", "r", encoding="utf8") as f, open("replaced", "w", encoding="utf8") as n:
        x = f.read()
        result = re.sub("[^A-Za-z\s]", "", x, 0, re.IGNORECASE | re.MULTILINE)
        n.write(result)


    hack_cipher("replaced")


if __name__ == "__main__":
    main()
