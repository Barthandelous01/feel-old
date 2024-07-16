#!/bin/env python3
# Copyright Caleb D.S. Brzezinski 2024
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pandas as pd
from datetime import datetime

# from stackoverflow:
# https://stackoverflow.com/questions/35794173/
num_words={
    '0':'zero',
    '1':'one',
    '2':'two',
    '3':'three',
    '4':'four',
    '5':'five',
    '6':'six',
    '7':'seven',
    '8':'eight',
    '9':'nine',
    '10':'ten',

    '11':'eleven',
    '12':'twelve',
    '13':'thirteen',
    '14':'fourteen',
    '15':'fifteen',
    '16':'sixteen',
    '17':'seventeen',
    '18':'eighteen',
    '19':'nineteen',

    '20':'twenty',
    '30':'thirty',
    '40':'fourty',
    '50':'fifty',
    '60':'sixty',
    '70':'seventy',
    '80':'eighty',
    '90':'ninety',
}
    
def num_2_words(num):
    if num <= 20: return num_words[str(num)]
    elif num % 10 == 0 and num < 100: return num_words[str(num)]
    elif num < 100: return num_words[str(num//10)+'0']+' '+num_words[str(num%10)]
    elif num % 100 == 0 and num < 1000: return  num_words[str(num//100)]+' '+'hundred'
    elif num < 1000: return num_words[str(num//100)]+' hundred and '+ num_2_words(num%100)
    elif num % 1000 == 0 and num < 10000: return num_words[str(num//1000)]+' '+'thousand'
    elif num < 10000: return num_words[str(num//1000)]+' thousand '+ num_2_words(num%1000)
    elif num == 10000: return 'ten thousand'
    else: return 'more than ten thousand'

def decades_since(date1, date2):
    # yes, we're doing dates as year integers. Deal with it.
    assert date1 < date2

    # get decade difference
    date1 -= date1 % 10
    date2 -= date2 % 10

    decades = (date2 - date1) // 10
    if decades != 1:
        plural = "s"
    else:
        plural = ""

    return("{} decade{} ago?".format(num_2_words(decades), plural))


def construct_sentence(film, date, response_fn):
    s = "Did you realize that " # note the extra space

    # note the extra space here too
    s += film + " came out "
    s += response_fn(date, datetime.now().year)

    return(s)

def make_range(age):
    import math

    Delta = 15 - math.sqrt(age)
    l = 16-Delta
    r = 16+Delta
    year = datetime.now().year
    lh = year - (age - l)
    rh = year - (age - r)
    return((lh,rh))

def pick_movie(arange, db):
    l,h = arange
    dbf = db[db['year'].isin(range(int(l),int(h)))]
    return(dbf.sample())

def main():
    age = int(input("How old are you? "))
    db = pd.read_csv("./movies.csv")
    film = pick_movie(make_range(age), db)

    # pandas shenanigans
    movie = str(film['original_title'].iloc[0])
    year = int(film['year'].iloc[0])

    print(construct_sentence(movie, year, decades_since))

if __name__ == "__main__":
    main()
