def extract(jobPath):

    # opens dat to read
    f = open(jobPath, 'r')

    content = []
    tsaiw_idx_f = []
    tsaiw_idx_m = []
    search_str1 = "   THE FOLLOWING TABLE IS PRINTED FOR ALL ELEMENTS WITH TYPE S4R AT THE INTEGRATION POINTS\n"
    search_str2 = "          THE ANALYSIS HAS BEEN COMPLETED\n"
    for (i, line) in enumerate(f):
        if search_str1 in line:
            tsaiw_idx_m.append(i-8)
        elif search_str2 in line:
            tsaiw_idx_f.append(i-7)
        content.append(line)
    tsai_idx = tsaiw_idx_m[1:] + tsaiw_idx_f

    tsaiw = []
    for idx in tsai_idx:
        twstr = content[idx].split()
        tsaiw.append(float(twstr[1]))
    max_tsaiw = max(tsaiw)

    return max_tsaiw