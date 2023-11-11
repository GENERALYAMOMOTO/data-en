with open("text_1_var_45", "r") as f:
    linses = f.readlines()

words_stat = {}

for line in linses:
    row_line = (line.strip()
                .replace('!',' ')
                .replace('?',' ')
                .replace(',',' ')
                .replace('.',' ')
                .strip())
    
    words = row_line.split(' ')

    for word in words:
        if word in words_stat:
            words_stat[word] += 1
        else:
            words_stat[word] = 1

words_stat = (dict(sorted(words_stat.items(), reverse=True, key=lambda item: item[1])))

with open("r_text_1_var_45", "w") as r:
    for k, v in words_stat.items():
        r.write(k + ' : ' +str(v) + '\n')