

# Need to store:

def opt_encoding_file(lines):
    return sum([(i + 1) * opt_encoding_line(line) for i, line in enumerate(lines)])

def extract_run_encoding_stats(line):
    if not line:
        return {}

    hits: dict[str, int] = {}
    first_char = line[0]
    run_length = 1

    def _add_info_to_hits(hits, first_char, run_length):
        run_id = f"{first_char}{run_length}"
        hits[run_id] = hits.get(run_id, 0) + 1
        return hits

    for i, char in enumerate(line[1:]):
        if char == first_char:
            run_length += 1

        if char != first_char:
            _add_info_to_hits(hits, first_char, run_length)
            first_char = char
            run_length = 1

    # add last
    _add_info_to_hits(hits, first_char, run_length)

    return hits


def encoding_cost(stat):
    run, occurences = stat
    replaced = occurences * len(run)
    added = len(run) + occurences
    # lower -> better, more gain from replacing this char
    return (added - replaced)


def encode_length(sorted_stats):
    encode_length = 0
    raw_length = 0
    idx = 0

    for stat in sorted_stats:
        run, oc = stat
        raw_length += oc * len(run)

        cost = encoding_cost(stat)

        if idx < 26 and cost < 0:
            encode_length += len(run) + oc
        else:
            encode_length += oc * len(run)

        idx += 1

    # check if actually worth once header ;; add
    return min(encode_length + 2, raw_length)



def opt_encoding_line(line):
    stats = extract_run_encoding_stats(line)
    stats = sorted(stats.items(), key=lambda x: encoding_cost(x))
    return encode_length(stats)


with open('input.txt', 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    print(opt_encoding_file(lines))


print(opt_encoding_line("A"))
print("exp 2: ", opt_encoding_line("A"))
print("exp 30 : ", opt_encoding_file(['A', 'BBCCBBCCBBCCBBCC']))
print("exp 8  : ", opt_encoding_line('BBCCBBCC'))
print("exp 14  : ", opt_encoding_line('BBCCBBCCBBCCBBCC'))


