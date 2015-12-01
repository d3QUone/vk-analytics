# -*- coding: cp1251 -*-
import os
import sys
from datetime import datetime

import requests


FILENAME = "_input.txt"
RES_DIR = "output"

def main():
    t = datetime.now()
    glob = 0
    groupNum = 1
    if not os.path.isfile(FILENAME):
        print 'No _input.txt file'
        sys.exit()
    if not os.path.isdir(RES_DIR):
        os.mkdir(RES_DIR)
    f = open(FILENAME, 'r')
    inp = f.readline()
    while inp != '':
        # prepare template
        p = parse(inp)
        g = open(os.path.join(RES_DIR, "{0}.html".format(p)), "w")
        g.write('<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>{0}</title>\n</head>\n<body>\n'
                '<h3 align="center"><a href="{1}" target="_blank">{0}</a></h3>'
                '<table width="50%" border="1" align="center"><tr align="center">'
                '<td width="15%">likes</td><td width="15%">comm</td><td width="15%">reposts</td><td>link</td></tr>'.format(p, inp))
        g.close()
        print '{0}. group name: {1}'.format(groupNum, p)
        groupNum += 1

        # prepare and tryout 
        ret = request_data(p, 0, 1)
        count = ret['response']['count']
        print 'num to parse: {0}\n'.format(count)
        offset = count//100 + 1
        output = []
        append = output.append
        for i in range(0, offset):
            posts = request_data(p, i*100, 100)
            for post in posts['response']['items']:
                try:
                    link = 'vk.com/{0}?w=wall-{1}_{2}'.format(p, post['owner_id'], post['id'])
                    comm = post['comments']['count']
                    like = post['likes']['count']
                    repo = post['reposts']['count']
                    
                    append([like, link, comm, repo])
                except Exception as ex:
                    print "Post-parsing exception: {0}".format(ex)
                glob += 1
        # sort by likes
        output.sort(reverse=True)
        # the result representing
        g = open(os.path.join(RES_DIR, "{0}.html".format(p)), "a")
        for i in range(0, len(output)):
            g.write('\n<tr align="center">\n<td>{0}</td>\n<td>{1}</td>\n<td>{2}'
                    '</td>\n<td><a href="https://{3}" target="_blank">Check it'
                    '</a></td>\n</tr>'.format(output[i][0], output[i][2], output[i][3], output[i][1]))
        g.write('</table>\n<br><div align="center"><a href="https://github.com/d3QUone/vk-analytics2" '
                'target="_blank">Follow me on GitHub!</a></div><br>\n</body>\n</html>')
        g.close()
        inp = f.readline()
        
    f.close()
    t = datetime.now() - t
    print '\nDone.'
    print '\nWorked = {0}\n\ntotal posts = {1}'.format(t, glob)
    with open('_stat.txt', 'w') as stat:
        stat.write('worked = {0}\n\ntotal posts = {1}'.format(t, glob))


def parse(st):
    start = 0
    end = len(st)
    out = ''
    for i in range(end):
        if start == 0 and st[i] == 'm':
            start = 1
        if start == 1 and st[i] == '/':
            start = 2
        elif start == 2: 
            out += st[i]
    end = len(out)-1
    if out[end] == '\n':
        out = out[:end]
    return out


def request_data(domain, offset=0, count=100):
    params = {
        "domain": domain,
        "offset": offset,
        "count": count,
        "v": "5.27"
    }
    r = requests.get("https://api.vk.com/method/wall.get", params=params, timeout=5.0)
    return r.json()


if __name__ == "__main__":
    main()
