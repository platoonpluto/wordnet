# -*- coding: utf-8 -*-

import traceback
from WordNetConsts import *

class DiskToMemory(object):
    def __init__(self):
        self.disk_to_memory = {}
    def get(self, k):
        if k not in self.disk_to_memory:
            return None
        return self.disk_to_memory[k]
    def set(self, k, v):
        self.disk_to_memory[k] = v
    def insert(self, k):
        self.disk_to_memory[k] = None

class Word(object):
    def __init__(self):
        self.lemma = None#	//word
        self.pos = None#			//part of speech
        self.synset_cnt = None#		//number of synsets that lemma is in
        self.p_cnt = None#			//number of different pointers that lemma has in all synsets containing it.
        self.ptr_symbol = []#	//a space seperated list of p_cnt pointers that lemma has in all synsets containing it.
        self.sense_cnt = None#		//redundant
        self.tagsense_cnt = None#	//number of senses of lemma that are ranked according to their frequency of occurrence in semantic concordance texts.
        self.synset_offset = None#	//bye offset of a synset containing lemma.这是在硬盘上的保存方式，在内存中使用<Synset *>向量来表示	
        self.synsets = []#
    def get_pos(self, ch):
        for idx in xrange(0, len(pos_key)):
            if ch == pos_key[idx]:
                return idx
        return -1
    def get_pointer_symbol(self, key):
        for idx in xrange(0, len(word_pointer_type)):
            if key == word_pointer_type[idx]:
                return idx
        return -1
    def parse_word(self, disk_to_mem, line):
        columns = line.strip().decode('utf-8').split(' ')
        try:
            idx = 0
            self.lemma = columns[0]
            idx += 1
            self.pos = self.get_pos(columns[idx])
            idx += 1
            self.synset_cnt = int(columns[idx])
            idx += 1
            self.p_cnt = int(columns[idx])
            idx += 1
            for cnt in xrange(0, self.p_cnt):
                self.ptr_symbol.append(self.get_pointer_symbol(columns[idx]))
                idx += 1
            self.sense_cnt = int(columns[idx])
            idx += 1
            self.tagsense_cnt = int(columns[idx])
            idx += 1
            for cnt in xrange(0, self.synset_cnt):
                offset = int(columns[idx])
                idx += 1
                self.synsets.append(offset)
                disk_to_mem.insert(offset)
        except:
            print line
            return -1
        return 0
    def print_info(self):
        print 'Word Info Begin:'
        print 'lemma:', self.lemma
        print 'pos:', self.pos
        print 'synset_cnt:', self.synset_cnt, ':'
        for cnt in xrange(0, self.synset_cnt):
            print self.synsets[cnt]
        print 'pointer cnt:', self.p_cnt, ':'
        for cnt in xrange(0, self.p_cnt):
            print self.ptr_symbol[cnt]
        print 'Word Info End'

class Pointer(object):
    def __init__(self):
        self.pointer_symbol = None
        self.synset_offset = None
        self.pos = None
        self.source = None
        self.target = None

class Synset(object):
    def __init__(self):
        self.synset_offset = None
        self.lex_filenum = None
        self.ss_type = None
        self.w_cnt = None
        self.word = []
        self.lex_id = []
        self.p_cnt = None
        self.ptr = []
        self.f_cnt = None       #当SS_VERB时有效
        self.frames_f_num = []       #当SS_VERB时有效
        self.frames_w_num = []       #当SS_VERB时有效
        self.gloss = None
        self.synset_id = None #//每个synset的ID，是为了区分形容词之间的antonym关系引入的
        self.distance_to_root = None #//当synset是名词时表示当前synset到整棵树根结点的位置
        self.antonym_set = set() #//当synset为形容词时表示当前head synset的反义词组成的集合
        self.parent = None #//当synset是名词时表示当前synset的父结点；当synset为形容词时表示当前synset的head synset
        self.children = [] #//当synset是名词是表示当前synset的孩子结点；当synset为形容词时表示当前synset的satellite synset
        self.antonym = None #//当synset为形容词时表示当前head synset的反义词
        self.derived = None #//当synset为副词时表示当前synset派生来的形容词synset
        self.to_string = None
    def get_sstype(self, ch):
        for idx in xrange(0, len(ss_type)):
            if ss_type[idx] == ch:
                return idx
        return -1
    def get_pos(self, ch):
        for idx in xrange(0, len(pos_key)):
            if pos_key[idx] == ch:
                return idx
        return -1
    def get_pointer_symbol(self, key):
        for idx in xrange(0, len(synset_pointer_type)):
            if key == synset_pointer_type[idx]:
                return idx
        return -1
    def parse_synset(self, disk_to_mem, line):
        columns = line.strip().decode('utf-8').split(' ')
        try:
            idx = 0
            self.synset_offset = int(columns[idx])
            idx += 1
            disk_to_mem.set(self.synset_offset, self)
            self.lex_filenum = int(columns[idx])
            idx += 1
            self.ss_type = self.get_sstype(columns[idx])
            idx += 1
            self.w_cnt = int(columns[idx], 16)
            idx += 1
            for cnt in xrange(0, self.w_cnt):
                word = columns[idx]
                self.word.append(word)
                idx += 1
                lex_id = columns[idx]
                self.lex_id.append(lex_id)
                idx += 1
            self.to_string = ','.join(self.word)
            self.p_cnt = int(columns[idx])
            idx += 1
            for cnt in xrange(0, self.p_cnt):
                ptr = Pointer()
                ptr.pointer_symbol = self.get_pointer_symbol(columns[idx])
                idx += 1
                ptr.synset_offset = int(columns[idx])
                idx += 1
                ptr.pos = self.get_pos(columns[idx])
                idx += 1
                source_target = columns[idx]
                idx += 1
                self.ptr.append(ptr)
            if self.ss_type == SS_VERB:
                self.f_cnt = int(columns[idx])
                idx += 1
                for cnt in xrange(0, self.f_cnt):
                    add_op = columns[idx]
                    idx += 1
                    self.frames_f_num.append(columns[idx])
                    idx += 1
                    self.frames_w_num.append(columns[idx])
                    idx += 1
            self.gloss = ' '.join(columns[idx:])
        except:
            print line
            print traceback.format_exc()
            return -1
        return 0
    def print_info(self):
        print 'Synset Info Begin:'
        print 'synset offset:', self.synset_offset
        print 'lex filenum:', self.lex_filenum
        print 'sstype:', self.ss_type
        print 'w_cnt:', self.w_cnt, ':'
        for idx in xrange(0, self.w_cnt):
            print self.word[idx], self.lex_id[idx]
        print 'p_cnt:', self.p_cnt, ':'
        for ptr in self.ptr:
            print ptr.pointer_symbol, ptr.synset_offset, ptr.pos
        print 'gloss:', self.gloss
        print 'Synset Info End'

class WordNet(object):
    def __init__(self):
        self.words_noun = []
        self.words_verb = []
        self.words_adj = []
        self.words_adv = []
        self.synsets_noun = []
        self.synsets_verb = []
        self.synsets_adj = []
        self.synsets_adv = []
        self.disk_to_mem_noun = DiskToMemory()
        self.disk_to_mem_verb = DiskToMemory()
        self.disk_to_mem_adj = DiskToMemory()
        self.disk_to_mem_adv = DiskToMemory()
        self.noun_roots = []
    def LoadWords(self, filename, disk_to_mem, words):
        myfile = open(filename)
        for line in myfile:
            if len(line) >= 2 and line[0] == ' ' and line[1] == ' ':
                continue
            w = Word()
            w.parse_word(disk_to_mem, line)
            words.append(w)
        myfile.close()
    def LoadSynsets(self, filename, disk_to_mem, synsets):
        myfile = open(filename)
        for line in myfile:
            if len(line) >= 2 and line[0] == ' ' and line[1] == ' ':
                continue
            s = Synset()
            s.parse_synset(disk_to_mem, line)
            synsets.append(s)
        myfile.close()
    def RefreshSynsetAddressToWords(self, words, disk_to_mem):
        for word in words:
            for idx in xrange(0, len(word.synsets)):
                offset = word.synsets[idx]
                word.synsets[idx] = disk_to_mem.get(offset)
    def RefreshSynsetAddressToSynsets(self, synsets, disk_to_mem):
        for synset in synsets:
            for idx in xrange(0, len(synset.ptr)):
                offset = synset.ptr[idx].synset_offset
                synset.ptr[idx].synset_offset = disk_to_mem.get(offset)
    def Init(self, dirpath):
        self.LoadWords(dirpath + "index.noun", self.disk_to_mem_noun, self.words_noun)
        self.LoadSynsets(dirpath + "data.noun", self.disk_to_mem_noun, self.synsets_noun)
        self.RefreshSynsetAddressToWords(self.words_noun, self.disk_to_mem_noun)
        self.RefreshSynsetAddressToSynsets(self.synsets_noun, self.disk_to_mem_noun)
        self.LoadWords(dirpath + "index.verb", self.disk_to_mem_verb, self.words_verb)
        self.LoadSynsets(dirpath + "data.verb", self.disk_to_mem_verb, self.synsets_verb)
        self.RefreshSynsetAddressToWords(self.words_verb, self.disk_to_mem_verb)
        self.RefreshSynsetAddressToSynsets(self.synsets_verb, self.disk_to_mem_verb)
        self.LoadWords(dirpath + "index.adj", self.disk_to_mem_adj, self.words_adj)
        self.LoadSynsets(dirpath + "data.adj", self.disk_to_mem_adj, self.synsets_adj)
        self.RefreshSynsetAddressToWords(self.words_adj, self.disk_to_mem_adj)
        self.RefreshSynsetAddressToSynsets(self.synsets_adj, self.disk_to_mem_adj)
        self.LoadWords(dirpath + "index.adv", self.disk_to_mem_adv, self.words_adv)
        self.LoadSynsets(dirpath + "data.adv", self.disk_to_mem_adv, self.synsets_adv)
        self.RefreshSynsetAddressToWords(self.words_adv, self.disk_to_mem_adv)
        self.RefreshSynsetAddressToSynsets(self.synsets_adv, self.disk_to_mem_adv)
    def BuildNounTree(self):
        for synset in self.synsets_noun:
            #synset.print_info()
            for ptr in synset.ptr:
                if ptr.pointer_symbol == 1 or ptr.pointer_symbol == 22:
                    synset.parent = ptr.synset_offset
                    ptr.synset_offset.children.append(synset)
        for synset in self.synsets_noun:
            if synset.parent == None:
                self.noun_roots.append(synset)
                synset.print_info()

wordnet = WordNet()
wordnet.Init("WordNet-3.0/dict/")
wordnet.BuildNounTree()

if __name__ == "__main__":
    dm = DiskToMemory()
    dm.insert(8)
    dm.set(8, 9)
    print dm.get(8)
    print dm.get(9)
    word = Word()
    print word.get_pos('a')
    print word.get_pos('w')
    print word.get_pointer_symbol("=")
    print word.get_pointer_symbol("hello")
    line = '''a_posteriori a 2 3 ! & ^ 2 0 00139126 00859350'''
    word.parse_word(dm, line)
    word.print_info()
    synset = Synset()
    print synset.get_pointer_symbol("!")
    print synset.get_pointer_symbol("hello")
    line = '''000015295416 28 n 01 rule 0 004 @ 15133621 n 0000 + 02586619 v 0102 ~i 15295603 n 0000 ~ 15298995 n 0000 | the duration of a monarch's or government's power; "during the rule of Elizabeth"'''
    synset.parse_synset(dm, line)
    synset.print_info()
    #wordnet = WordNet()
    #wordnet.Init("WordNet-3.0/dict/")
    #wordnet.BuildNounTree()
    print 'done...'
