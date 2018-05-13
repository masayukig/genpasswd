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
import re
import sqlite3
import subprocess
import sys

parser = argparse.ArgumentParser(description='Generate a memorable password.')
parser.add_argument('--count', default='3', type=int)
args = parser.parse_args()
# FIXME: SQLite3 path should be customizable

dbfile = path.dirname(path.abspath(__file__)) + '/data/ejdict.sqlite3'

def main(args=args):

    with closing(sqlite3.connect(dbfile)) as conn:
        c = conn.cursor()
        sql = "select word from items order by random() limit ?"
        words = [re.sub("[-\"' !.,]", '', row[0]).lower()
                 for row in c.execute(sql, (args.count,))]

    #print(words)
    print('-'.join(words))


if __name__ == '__main__':
    main()
