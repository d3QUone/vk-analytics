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
        print 'No input file'
        quit()

    inp = f.readline()
    while inp != '':
        # prepare template
        p = parse(inp) #group link
        g = open(p + '.html', 'w')
        g.write('<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>'+p+\
                '</title>\n</head>\n<body>\n'+\
                '<h3 align="center"><a href="'+inp+'" target="_blank">'+p+'</a></h3>'+\
                '<table width="50%" border="1" align="center"><tr align="center">'+\
                '<td width="15%">likes</td><td width="15%">comm</td><td width="15%">reposts</td><td>link</td></tr>')
        g.close
        print str(groupNum)+'. group name: ' + p
        groupNum += 1

        # prepare and tryout 
        ret = getA(p, 0, 1)
        count = ret['response']['count']
        print 'num to parse:', str(count), '\n'
        offset = count//100 + 1
        output = []
        for i in range(0, offset):
            posts = getA(p, i*100, 100)
            for post in posts['response']['items']:
                #print post, '\n'
                try:
                    link = 'vk.com/'+p+'?w=wall'+str(post['from_id']) + '_' + str(post['id'])

                    comm = post['comments']['count']
                    like = post['likes']['count']
                    repo = post['reposts']['count']
                    
                    output.append({'link': link, 'comm': comm, 'like': like, 'repo': repo})
                except BaseException as ex:
                    print ex
                glob += 1

        # sort by likes 
        a = [[o['like'], o['link'], o['comm'], o['repo']] for o in output] 
        a.sort(reverse=True)

        # the result representing
        g = open(p + '.html', 'a')
        for i in range(0, len(a)):
            g.write('\n<tr align="center">\n<td>'+ str(a[i][0]) +\
                    '</td>\n<td>'+str(a[i][2])+\
                    '</td>\n<td>'+str(a[i][3])+\
                    '</td>\n<td><a href="https://'+a[i][1]+\
                    '" target="_blank">Check it' +\
                    '</a></td>\n</tr>')            
        g.write('</table>\n<br><div align="center"><a href="https://github.com/d3QUone/vk-analytics2" '+\
                'target="_blank">Follow me on GitHub!</a></div><br>\n</body>\n</html>')
        g.close
        inp = f.readline()
        
    f.close
    print '\nDone.'
    t = datetime.now() - t
    print '\nWorked = ' + str(t) + '\n\ntotal posts = ' + str(glob)
    stat = open('_stat.txt', 'w')
    stat.write('worked = ' + str(t) + '\n\ntotal posts = ' + str(glob))
    stat.close


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
    response = urllib.urlopen('https://api.vk.com/method/wall.get?domain='+dom+\
                              '&offset='+str(off)+'&count=' + str(cou) + '&v=5.26')
    return json.load(response)

                              
main()
