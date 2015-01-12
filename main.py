# -*- coding: cp1251 -*-
import urllib
import json
from datetime import datetime

def main():
    # for stats
    t = datetime.now()
    glob = 0
    groupNum = 1

    # check input
    try:
        f = open('_input.txt', 'r')
    except:
        print 'No _input.txt file'
        quit()

    inp = f.readline()
    while inp != '':
        # prepare template
        p = parse(inp) #group link
        g = open('output/{0}.html'.format(p), 'w')
        g.write('<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>{0}</title>\n</head>\n<body>\n'+\
                '<h3 align="center"><a href="{1}" target="_blank">{0}</a></h3>'+\
                '<table width="50%" border="1" align="center"><tr align="center">'+\
                '<td width="15%">likes</td><td width="15%">comm</td><td width="15%">reposts</td><td>link</td></tr>'.format(p, inp))
        g.close()
        print '{0}. group name: {1}'.format(groupNum, p)
        groupNum += 1

        # prepare and tryout 
        ret = getA(p, 0, 1)
        count = ret['response']['count']
        print 'num to parse:{0}\n'.format(count)
        offset = count//100 + 1
        output = []
        append = output.append
        for i in range(0, offset):
            posts = getA(p, i*100, 100)
            for post in posts['response']['items']:
                #print post, '\n'
                try:
                    link = 'vk.com/{0}?w=wall-{1}_{2}'.format(p, post['owner_id'], post['id'])
                    comm = post['comments']['count']
                    like = post['likes']['count']
                    repo = post['reposts']['count']
                    
                    append([like, link, comm, repo])
                except BaseException as ex:
                    print ex
                glob += 1

        # sort by likes 
        a.sort(reverse=True)

        # the result representing
        g = open('output/{0}.html'.format(p), 'a')
        for i in range(0, len(a)):
            g.write('\n<tr align="center">\n<td>{0}</td>\n<td>{1}</td>\n<td>{2}'+\
                    '</td>\n<td><a href="https://{3}" target="_blank">Check it' +\
                    '</a></td>\n</tr>'.format(a[i][0], a[i][2], a[i][3], a[i][1]))            
        g.write('</table>\n<br><div align="center"><a href="https://github.com/d3QUone/vk-analytics2" '+\
                'target="_blank">Follow me on GitHub!</a></div><br>\n</body>\n</html>')
        g.close
        inp = f.readline()
        
    f.close
    t = datetime.now() - t
    print '\nDone.'
    print '\nWorked = {0}\n\ntotal posts = {1}'.format(t, glob)
    stat = open('_stat.txt', 'w')
    stat.write('worked = {0}\n\ntotal posts = {1}'.format(t, glob))
    stat.close()


def parse(st):
    i = start = 0
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


def getA(dom, off=0, cou=100):
    response = urllib.urlopen('https://api.vk.com/method/wall.get?domain={0}&offset={1}&count={2}&v=5.26'.format(dom, off, cou))
    return json.load(response)

                              
main()
