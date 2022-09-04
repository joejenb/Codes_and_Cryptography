import paq
from wordfreq import top_n_list
import sys

lz_file = sys.argv[1]
file_name = lz_file[:-3]
tex_file = file_name + "-decoded.tex"

def de_proc(pre_proc):
    words = [word.lower() for word in top_n_list('en', 82000)]
    used_words = words.copy()
    allowable = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]

    fo_symbs = [chr(i) for i in range(128, 137)]
    s_symbs = [chr(i) for i in range(137, 146)]
    t_symbs = [chr(i) for i in range(146, 155)]
    f_symbs = [chr(i) for i in range(155, 255)]

    ciphertexts = []

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

    seperator = pre_proc.index(chr(255))

    swaps = []
    if pre_proc[seperator + 2:]:
        swaps = pre_proc[seperator + 2:].split(' ')

    substituted = pre_proc[:seperator].split(' ')
    for ind in range(len(swaps)-2, -2, -2):
        #swaps stores the indexes of swapped words in encoded form 
        #swapped words already have the correct indicies just need to replace them with the correct text
        under = swaps[ind]
        over = swaps[ind+1]
        under_coded = ciphertexts.index(under)
        over_coded = ciphertexts.index(over)
        for ind in range(len(substituted)):
            if substituted[ind] == under:
                substituted[ind] = over
            elif substituted[ind] == over:
                substituted[ind] = under

    #Now have text using original dictionary
    #Get text with correct words -> subing in the wrong words when following word is in caps
    for ind in range(len(substituted)):
        if substituted[ind] in ciphertexts:
            substituted[ind] = words[ciphertexts.index(substituted[ind])]

    #Get text with correct flags applied
    ind = 0
    while ind < len(substituted):
        #Leave next symbol be
        if substituted[ind]:
            if substituted[ind][0] == '/':
                substituted[ind] = substituted[ind][1]
            #Capitalise first letter of next word
            elif substituted[ind] == '~':
                substituted[ind + 1] = substituted[ind + 1][0].upper() + substituted[ind + 1][1:]
                del substituted[ind]
            #Capitalise whole of next word
            elif substituted[ind] == '`':
                substituted[ind + 1] = substituted[ind + 1].upper()
                del substituted[ind]
        ind += 1

    substituted = ' '.join(substituted)
    out_stream = list(substituted)
    ind = 0
    while ind < len(out_stream):
        #Must delete spaces either side of punctuation -> must be done after flags -> Easier once all spaces have been added back in
        if out_stream[ind] != ' ':
            if out_stream[ind] not in allowable:
                del out_stream[ind+1] 
                del out_stream[ind-1]
        ind += 1

    return ''.join(out_stream)
    
with open(tex_file, "wb") as tex_data, open(lz_file, "rb") as lz_data:
    compressed = lz_data.read()
    pre_proc = paq.decompress(compressed)
    pre_proc = pre_proc.decode()
    plaintext = de_proc(pre_proc)
    tex_data.write(bytes(plaintext, 'utf-8'))
    
