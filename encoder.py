from wordfreq import top_n_list
import paq
import sys

tex_file = sys.argv[1]
file_name = tex_file[:-4]
lz_file = file_name + ".lz"


def part_6(plaintext):
    #doing this removes ALL spaces -> Must record all instances where have more than one space -> default is one space
    plaintext = plaintext.split(' ')
    words = [word.lower() for word in top_n_list('en', 82000)]
    swapped = [chr(255)]
    frequencies = {word: 0 for word in words} 

    for word in plaintext:
        if word.lower() in words:
            frequencies[word.lower()] += 1

    ideal_words = words.copy()
    ideal_words.sort(reverse=True, key= lambda word: frequencies[word])

    fo_symbs = [chr(i) for i in range(128, 137)]
    s_symbs = [chr(i) for i in range(137, 146)]
    t_symbs = [chr(i) for i in range(146, 155)]
    f_symbs = [chr(i) for i in range(155, 255)]

    ciphertexts = []
    token_stream = []
    flags = ['~', '`', '/']

    for fsymb in f_symbs:
        ciphertexts.append(fsymb)

    for fsymb in f_symbs:
        for ssymb in s_symbs:
            ciphertexts.append(fsymb + ssymb)

    for fsymb in f_symbs:
        for ssymb in s_symbs:
            for tsymb in t_symbs:
                ciphertexts.append(fsymb + ssymb + tsymb)

    for fsymb in f_symbs:
        for ssymb in s_symbs:
            for tsymb in t_symbs:
                for fosymb in fo_symbs:
                    ciphertexts.append(fsymb + ssymb + tsymb + fosymb)
    
    default_len = {words[i]: len(ciphertexts[i] * frequencies[words[i]]) for i in range(len(ideal_words))}
    lengths = {ideal_words[i]: [len(ciphertexts[i] * frequencies[ideal_words[i]]), default_len[ideal_words[i]]] for i in range(len(ideal_words))}

    for word in plaintext:
        l_word = word.lower()
        #Add check for no capitals in the word itself
        if l_word in words and ((l_word == word) or (word.upper() == word) or (l_word[0].upper()+l_word[1:] == word)):
            encoded = ciphertexts[words.index(l_word)]
            if l_word != word:
                if word.upper() == word:
                    token_stream.append('`')
                elif l_word[0].upper()+l_word[1:] == word:
                    token_stream.append('~')
            token_stream.append(encoded)
        else:
            if word in flags:
                word = '/' + word
            token_stream.append(word)

    org_len = len(' '.join(token_stream)) 
    while True:
        #One where frequency is alot higher than in standard dict
        under = max(lengths, key=lambda word: lengths[word][1] - lengths[word][0])
        under_coded = ciphertexts[words.index(under)]
        del lengths[under]
        #One where frequency is alot lower than in standard dict
        over = max(lengths, key=lambda word: lengths[word][0] - lengths[word][1])
        #Gives the ciphertext that would usually correspond to the word for standard frequency
        #The position of this in ciphertexts is the same as over in words -> swap words in words so symbols switched
        over_coded = ciphertexts[words.index(over)]
        del lengths[over]
        improved_token_stream = token_stream.copy()
        new_swapped = swapped.copy()
        #Swap useage of symbols
        for ind in range(len(improved_token_stream)):
            if improved_token_stream[ind] == under_coded:
                improved_token_stream[ind] = over_coded
            elif improved_token_stream[ind] == over_coded:
                improved_token_stream[ind] = under_coded
        new_swapped.append(under_coded)
        new_swapped.append(over_coded)
        if len(' '.join(improved_token_stream)+' '.join(new_swapped)) < len(' '.join(token_stream)+' '.join(swapped)):
            token_stream = improved_token_stream.copy()
            swapped = new_swapped.copy()
        else:
            break

    out_stream = ' '.join(token_stream) + ' '.join(swapped)
    return out_stream


def sep_punc(plaintext):
    allowable = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
    new_plain = '' 
    for symb in plaintext:
        to_add = symb
        if symb not in allowable and symb != " ":
                to_add = " " + to_add + " "
        new_plain += to_add
    return new_plain

   
'''Could insert a space in front of every bit of punctuation and then split'''
with open(tex_file, "rb") as tex_data:
    text = tex_data.read().decode()
    #text_w = text.encode("ascii", "ignore")
    #text = text_w.decode()

    with open(lz_file, 'wb') as lz_data:
        pre_proc = sep_punc(text)
        pre_proc = part_6(pre_proc)
        proc_paq_data = paq.compress(bytes(pre_proc, 'utf-8'))
        lz_data.write(proc_paq_data)

    #tex_data.seek(0)
    #tex_data.write(text_w)
    #tex_data.truncate()

