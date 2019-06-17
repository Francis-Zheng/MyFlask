from pyhanlp import *
from jpype import *

class mySegment:
    def __init__(self):
        self.Nature = SafeJClass("com.hankcs.hanlp.corpus.tag.Nature")
        self.IndexTokenizer = SafeJClass("com.hankcs.hanlp.tokenizer.IndexTokenizer")
        self.NLPTokenizer = SafeJClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
        self.KeywordExtractor = SafeJClass("com.hankcs.hanlp.summary.KeywordExtractor")

    def termToWord(self, term):
        term = term.word
        return term

    def segmentFilter(self, query_str)-> list:

        term_list = self.NLPTokenizer.segment(query_str)
        segment_list = list(filter(lambda term: term.nature != self.Nature.w
                                 and term.nature != self.Nature.c
                                 and term.nature != self.Nature.p
                                 and term.nature != self.Nature.uj
                                 and term.nature != self.Nature.ul
                                 and term.nature != self.Nature.ud
                                 and term.nature != self.Nature.r, term_list))
        segment_list = list(map(self.termToWord, segment_list))
        #for term in segment_list:
        #    print(term)

        return segment_list

    # 按照词频反向排序
    def sort_by_value(self, d):
        items = d.items()
        backitems = [[v[1], v[0]] for v in items]
        backitems.sort(reverse=True)
        return [backitems[i][1] for i in range(0, len(backitems))]

if __name__ == "__main__":
    str1 = "江西鄱阳湖干枯，中国最大淡水湖变成大草原"
    str2 = "攻城狮逆袭单身狗，迎娶白富美，走上人生巅峰"
    test = mySegment()
    test.segmentFilter(str2)