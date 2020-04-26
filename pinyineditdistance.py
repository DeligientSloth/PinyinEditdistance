import pypinyin
from pypinyin import pinyin

def getApproximateShengmuMap():
    approximate_shengmu = [('l', 'n'),('z', 'zh'), ('c', 'ch'),
                           ('s', 'sh'), ('f', 'fh')]
    approximate_shengmu2 = [(_[1], _[0]) for _ in approximate_shengmu]
    approximate_shengmu+=approximate_shengmu2
    return {_[0]:_[1] for _ in approximate_shengmu}

def getApproximateYunmuMap():
    approximate_yunmu = [('in', 'ing'), ('en', 'eng'), ('an', 'ang'),
                         ('uang', 'uan'), ('ang', 'ong'), ('si', 'ci')]
    approximate_yunmu2 = [(_[1], _[0]) for _ in approximate_yunmu]
    approximate_yunmu += approximate_yunmu2
    return {_[0]: _[1] for _ in approximate_yunmu}

def pinyin_distance(pinyin1, shengmu1, yunmu1, pinyin2, shengmu2, yunmu2):
    tone1, tone2 = pinyin1[-1], pinyin2[-1]
    pinyin1, pinyin2 = pinyin1[:-1], pinyin2[:-1]
    shengmuMap = getApproximateShengmuMap()
    yunmuMap = getApproximateYunmuMap()
    if pinyin1==pinyin2:
        if tone1==tone2:
            return 0
        else:
            return 0.5  # 修改读音即可
    if shengmu1==shengmu2 and yunmu1!=yunmu2:
        if yunmu1 in yunmuMap:
            if yunmu2==yunmuMap[yunmu1]:
                return 0.5  # 修改一个类似的韵母即可
            else:
                return 1    # 需要把韵母修改掉，而且读音不类似，相当于修改这个词
    elif shengmu1!=shengmu2 and yunmu1==yunmu2:
        if shengmu1 in shengmuMap:
            if shengmu2==shengmuMap[shengmu1]:
                return 0.5
            else:
                return 1
    else:
        #  声母和韵母都不一致
        if shengmu1 in shengmuMap and yunmu1 in yunmuMap:
            if shengmuMap[shengmu1]==shengmu2 and yunmuMap[yunmu1]==yunmu2:
                return 1   # 声母和韵母都是修改一个类似的读音 0.5+0.5
            elif shengmuMap[shengmu1]==shengmu2:
                return 1.5     # 修改一个类似的声母和一个韵母 0.5+1
            elif yunmuMap[yunmu1]==yunmu2:
                return 1.5
            else:
                return 2    # 修改声母和韵母
        elif shengmu1 in shengmuMap:
            if shengmuMap[shengmu1]==shengmu2:
                return 1
            else:
                return 2
        elif yunmu1 in yunmuMap:
            if yunmuMap[yunmu1]==yunmu2:
                return 1
            else:
                return 2
        else:
            return 2




def pinyin_editdistance(str1, str2):

    pinyins1 = pinyin(str1, style=pypinyin.TONE3)
    shengmus1 = pinyin(str1, style=pypinyin.INITIALS)
    yunmus1 = pinyin(str1, style=pypinyin.FINALS)
    pinyins2 = pinyin(str2,  style=pypinyin.TONE3)
    shengmus2 = pinyin(str2, style=pypinyin.INITIALS)
    yunmus2 = pinyin(str2, style=pypinyin.FINALS)

    n, m = len(pinyins1), len(pinyins2)

    dp = [[0 for j in range(m+1)] for i in range(n+1)]
    for i in range(1, n+1):
        dp[i][0] = i
    for j in range(1, m+1):
        dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            pinyin1, shengmu1, yunmu1 = pinyins1[i - 1][0], shengmus1[i - 1][0], yunmus1[i - 1][0]
            pinyin2, shengmu2, yunmu2 = pinyins2[i - 1][0], shengmus2[i - 1][0], yunmus2[i - 1][0]
            distance = pinyin_distance(pinyin1, shengmu1, yunmu1, pinyin2, shengmu2, yunmu2)
            dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])+distance
    return dp[n][m]


print(pinyin_editdistance('苹果', '苹国'))