# -*- encoding: UTF-8 -*-
r"""
#
# Author: Laimonas Vėbra, 2016
#
__numbertext__

# Digits
^0                 "nulis"
1                  "vienas"
2                  "du"
3                  "trys"
4                  "keturi"
5                  "penki"
6                  "šeši"
7                  "septyni"
8                  "aštuoni"
9                  "devyni"

# Teens
11                 "vienuolika"
12                 "dvylika"
13                 "trylika"
1([4-9])           "$1|olika"

# Tens
10                 "dešimt"
2(\d)              "dvidešimt $1"
3(\d)              "trisdešimt $1"
([4-9])(\d)        "$1|asdešimt $2"

# Exponents
(\d)(\d\d)         "$1 šimt$(-as:\1) $2"
(\d{1,3})(\d{3})   "$1 tūkstan$(-tis:\1) $2"
(\d{1,3})(\d{6})   "$1 milijon$(-as:\1) $2"
(\d{1,3})(\d{9})   "$1 milijard$(-as:\1) $2"
(\d{1,3})(\d{12})  "$1 trilijon$(-as:\1) $2"
(\d{1,3})(\d{15})  "$1 kvadrilijon$(-as:\1) $2"
(\d{1,3})(\d{18})  "$1 kvintilijon$(-as:\1) $2"


#############################
# Inflection: case endings  #
#############################
# (NOTE: the order of number match regexes is important)

-as?:\d?(?:1\d|\d?0)         "ų"      # genitive, plural      :šimt-ų, rupij-ų
-as:\d?[02-9]?[2-9]          "ai"     # nominative, plural    :šimt-ai

-tis:\d?(?:1\d|\d?0)         "čių"    # genitive, plural      :tūkstan-čių
-tis:\d?[02-9]?[2-9]         "čiai"   # nominative, plural    :tūkstan-čiai

-(?:is|ė):\d?(?:1\d|\d?0)    "ių"     # genitive, plural      :doler-ių, er-ių
-is:\d?[02-9]?[2-9]          "iai"    # nominative, plural    :doler-iai

-a:\d?[02-9]?[2-9]           "os"     # nominative, plural    :rupij-os
-ė:\d?[02-9]?[2-9]           "ės"     # nominative, plural    :er-ės

# what's left (\d?[02-9]?1); canonical form: no change
-(.+?):.+                    "\1"     # nominative, singular  :šimt-as, tūkstan-tis, doler-is, er-ė, rupij-a


# Gender (last numeral word ending change):
__G(?:-[aė]|~f):(.+)as       "\1a"    # vien-as -> vien-a
__G(?:-[aė]|~f):(.*)du       "\1dvi"  # du -> dvi
__G(?:-[aė]|~f):(.+)i        "\1ios"  # ketur-i, ..., devyn-i -> -ios
__G.+?:(.+)                  "\1"     # all other cases: no change

# Currency (alt.) name
__N:(.+)                     "\1"     # full (currency) name
__N~:(.*\b(.+))              "\2"     # short name (last word)

# Negative numbers
[-−](\d+)                    "minus |$1"

# Decimals
([-−]?\d+)[.,]               "$1| taškas"
([-−]?\d+[.,]\d*)(\d)        "$1| |$2"


##############
# Currencies #
##############

# Template regexes/"functions"
# Args: [~]{number}, {base_unit}{-case_var1}
#       [~]{number}, {base_unit}{-case_var1}, {sub_unit}{-case_var2}
#
#     [~] $1: currency alt. name; short (with ~). 
#     number: 
#         $2: whole (with minus sign), 
#         $3: last two digits of integer part (for inflection)
#         [$4]: fractional part 
#     base_unit: $5 | $4; without ending
#     case_var1: $6 | $5; case ending
#     sub_unit:  $7; without ending
#     case_var2: $8; case ending
#
CUR:(.+?[.,])(\d)(,.+)                                                               "$(CUR:\1\20\3)"  # frac. tens fix: ,2 -> 0,20
CUR:\s*(~?)\s([-−]?\d*?(\d?\d)),\s*(?u)(.+?)(-\w+|~f?),.+                            "$(__G\5:|$2) $(__N\1:\4)$(\5:\3)"
CUR:\s*(~?)\s([-−]?\d*?(\d?\d))[.,](\d\d),\s*(?u)(.+?)(-\w+|~f?),\s*(\w+)(-\w+|~f?)  "$(__G\6:|$2) $(__N\1:\5)$(\6:\3) |$(__G\8:|$4) \7$(\8:\4)"


# '-' denotes inflectional word/ending (ending itself determines numeral gender) 
# '~' denotes non inflectional word 
# (default numeral gender is masculine; for feminine append '~f', e.g.: tiyn~f)
USD(.+) $(CUR: \1, JAV doler-is, cent-as)
EUR(.+) $(CUR: \1, eur-as, cent-as)
JPY(.+) $(CUR: \1, Japonijos jen-a, sen-a)
GBP(.+) $(CUR: \1, Didžiosios Britanijos svar-as, pens-as)
AUD(.+) $(CUR: \1, Australijos doler-is, cent-as)
CHF(.+) $(CUR: \1, Šveicarijos frank-as, santim-as)
CAD(.+) $(CUR: \1, Kanados doler-is, cent-as)
MXN(.+) $(CUR: \1, Meksikos pes-as, sentav-as)
CNY(.+) $(CUR: \1, Kinijos juan-is, fen-as)
NZD(.+) $(CUR: \1, Naujosios Zelandijos doler-is, cent-as)
RUB(.+) $(CUR: \1, Rusijos rubl-is, kapeik-a)
HKD(.+) $(CUR: \1, Honkongo doler-is, cent-as)
SGD(.+) $(CUR: \1, Singapūro doler-is, cent-as)
TRY(.+) $(CUR: \1, Turkijos lir-a, kuruš-as)
KRW(.+) $(CUR: \1, Pietų Korėjos von-as, jeon-as)
ZAR(.+) $(CUR: \1, Pietų Afrikos Respublikos rand-as, cent-as)
BRL(.+) $(CUR: \1, Brazilijos real-as, sentav-as)
INR(.+) $(CUR: \1, Indijos rupij-a, pais-a)

SEK(.+) $(CUR: \1, Švedijos kron-a, er-ė)
NOK(.+) $(CUR: \1, Norvegijos kron-a, er-ė)
DKK(.+) $(CUR: \1, Danijos kron-a, er-ė)

PLN(.+) $(CUR: \1, Lenkijos zlot-as, graš-is)
CZK(.+) $(CUR: \1, Čekijos kron-a, haler-as)
HRK(.+) $(CUR: \1, Kroatijos kun-a, lip-a)
RSD(.+) $(CUR: \1, Serbijos dinar-as, par-a)
HUF(.+) $(CUR: \1, Vengrijos forint-as, filer-is)
BGN(.+) $(CUR: \1, Bulgarijos lev-as, stotink-a)
RON(.+) $(CUR: \1, Rumunijos lėj-a, ban-as)

BYR(.+) $(CUR: \1, Baltarusijos rubl-is, kapeik-a)
UAH(.+) $(CUR: \1, Ukrainos grivin-a, kapeik-a)
KZT(.+) $(CUR: \1, Kazachstano teng-ė, tiyn~)
AMD(.+) $(CUR: \1, Armėnijos dram-as, lum-a)
AZN(.+) $(CUR: \1, Azerbaidžano manat-as, kjapik-as)
GEL(.+) $(CUR: \1, Gruzijos lar-is, tetr-is)

# Historical
EEK(.+) $(CUR: \1, Estijos kron-a, cent-as)
LTL(.+) $(CUR: \1, Lietuvos lit-as, cent-as)
LVL(.+) $(CUR: \1, Latvijos lat-as, santim-as)


help "Currency \(alt.\) name \(full/short~\): „CUR[~]“, eg.: „LTL“ -> „vienas Lietuvos litas“, „LTL~“ -> „vienas litas“."
"""
from __future__ import unicode_literals

