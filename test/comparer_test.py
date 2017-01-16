# -*- encoding:utf-8 -*-

from comparer.comparer import WordCompare

from verify_new22 import stringdiffanalysis


def word_compare_test():
    left = "北京市朝阳区东四环中路78号楼大成国际A2-1009"
    right = "9北京市朝阳区东四环中路78号楼大成国际A21009123123"

    # print WordCompare(left,right).get_compare_result()

    left_tokens = list(left.decode("utf-8"))
    right_tokens = list(right.decode("utf-8"))
    i = 0
    while i < len(left_tokens):
        token = left_tokens[i]
        if token in right_tokens:
            left_tokens.remove(token)
            right_tokens.remove(token)
        else:
            i += 1

    print left_tokens
    print right_tokens

def compare_test():
    left = "北京市朝阳区东四环中路78号楼大成国际A2-1009"
    right = "9北京市朝阳区东四环中路78号楼大成国际A21109"
    left_tokens = list(left.decode("utf-8"))
    right_tokens = list(right.decode("utf-8"))
    ana = stringdiffanalysis(" ".join(left_tokens)," ".join(right_tokens))

    print ana.calclate_diff_lcs2()
    print ana._srcstring
    print ana._dststring
    print ana._diffstring
    print ana._errcount
    print ana._addcount
    print ana._subcount
    print ana._samecount
    print ana._allcount
    print ana._cer


if __name__ == "__main__":
    compare_test()