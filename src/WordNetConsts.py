# -*- coding: utf-8 -*-

pos_key = ["n", "v", "a", "r"]
POS_NOUN = 0
POS_VERB = 1
POS_ADJ = 2
POS_ADV = 3
POS_UNKNOWN = -1
word_pointer_type = [
"!",			#/* 1 ANTPTR */
"@",			#/* 2 HYPERPTR */
"~",			#/* 3 HYPOPTR */
"*",			#/* 4 ENTAILPTR */
"&",			#/* 5 SIMPTR */
"#m",			#/* 6 ISMEMBERPTR */
"#s",			#/* 7 ISSTUFFPTR */
"#p",			#/* 8 ISPARTPTR */
"%m",			#/* 9 HASMEMBERPTR */
"%s",			#/* 10 HASSTUFFPTR */
"%p",			#/* 11 HASPARTPTR */
"%",			#/* 12 MERONYM */
"#",			#/* 13 HOLONYM */
">",			#/* 14 CAUSETO */
"<",			#/* 15 PPLPTR */
"^",			#/* 16 SEEALSO */
"\\",			#/* 17 PERTPTR */
"=",			#/* 18 ATTRIBUTE */
"$",			#/* 19 VERBGROUP */
"+",		  #/* 20 NOMINALIZATIONS */
";",			#/* 21 CLASSIFICATION */
"-"				#/* 22 CLASS */
]

ss_type = ['n', 'v', 'a', 'r', 's']
SS_NOUN = 0
SS_VERB = 1
SS_ADJ = 2
SS_ADV = 3
SS_SATELLITE = 4
SS_UNKNOWN = -1
synset_pointer_type = [
"!",			#/* 1 ANTPTR */
"@",			#/* 2 HYPERPTR */
"~",			#/* 3 HYPOPTR */
"*",			#/* 4 ENTAILPTR */
"&",			#/* 5 SIMPTR */
"#m",			#/* 6 ISMEMBERPTR */
"#s",			#/* 7 ISSTUFFPTR */
"#p",			#/* 8 ISPARTPTR */
"%m",			#/* 9 HASMEMBERPTR */
"%s",			#/* 10 HASSTUFFPTR */
"%p",			#/* 11 HASPARTPTR */
"%",			#/* 12 MERONYM */
"#",			#/* 13 HOLONYM */
">",			#/* 14 CAUSETO */
"<",			#/* 15 PPLPTR */
"^",			#/* 16 SEEALSO */
"\\",			#/* 17 PERTPTR */
"=",			#/* 18 ATTRIBUTE */
"$",			#/* 19 VERBGROUP */
"+",      #/* 20 NOMINALIZATIONS */
";",			#/* 21 CLASSIFICATION */
"-",			#/* 22 CLASS */
"@i",			#// 23 instance hypernym
"~i",			#// 24 instance hyponym
";c",			#// 25 domain of synset - TOPIC
"-c",			#// 26 member of this domain - TOPIC
";r",			#// 27 domain of synset - REGION
"-r",			#// 28 member of this domain - REGION
";u",			#// 29 domain of synset - USAGE
"-u"			#// 30 member of this domain - USAGE
]

