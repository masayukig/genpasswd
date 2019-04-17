#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
from builtins import input
from contextlib import closing
from os import path
import random
import re
import sqlite3
import subprocess
import sys

parser = argparse.ArgumentParser(description='Generate a memorable password.')
parser.add_argument('--count', '-c', default='3', type=int)
parser.add_argument('--min', '-m', default='4', type=int)
parser.add_argument('--max', '-x', default='8', type=int)
parser.add_argument('--lower', '-l', default=False, action='store_true')
parser.add_argument('--join-string', '-j', default='', type=str)
parser.add_argument('--digits', '-d', default=3, type=int)
args = parser.parse_args()
# FIXME: SQLite3 path should be customizable

dbfile = path.dirname(path.abspath(__file__)) + '/data/ejdict.sqlite3'

def main(args=args):

    with closing(sqlite3.connect(dbfile)) as conn:
        c = conn.cursor()
        sql = "select word from items where length(word) >= ? " \
        "and length(word) <= ? and word not like '%-%' " \
        "and word not like '%\"%' and word not like \"%'%\" " \
        "and word not like '%,%' and word not like '%!%' " \
        "and word not like '%.%' and word not like '% %' " \
        "and word not like '%(%' and word not like '%)%' " \
        "and word not like '%/%' " \
        "order by random() limit ?"
        if args.lower:
            words = [re.sub("[-\"' !.,()/]", '', row[0]).lower()
                    for row in c.execute(sql, (args.min, args.max, args.count,))]
        else:
            words = [re.sub("[-\"' !.,()/]", '', row[0]).lower().capitalize()
                    for row in c.execute(sql, (args.min, args.max, args.count,))]

    password = args.join_string.join(words)
    if args.digits:
        rand_digits = format(random.randint(0, 10**args.digits - 1),
            str('0') + str(args.digits))
        password = args.join_string.join([password, rand_digits])

    print(password)


if __name__ == '__main__':
    main()
