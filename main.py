import urllib
import json

def main():
    try:
        f = open('_input.txt', 'r')
    except:
        f = open('_input.txt', 'w+')
        print 'No input file'
        
    inp = f.readline()
    while inp != '':
        p = parse(inp)
        g = open(p + '.html', 'w')
        g.write('<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>'+p+\
                '</title>\n</head>\n<body>\n'+\
                '<h3 align="center"><a href="'+inp+'" target="_blank">'+p+'</a></h3>'+\
                '<table width="50%" border="1" align="center"><tr align="center">'+\
                '<td width="15%">likes</td><td width="15%">reposts</td><td width="15%">comm</td><td>link</td></tr>')
        print 'group = ' + p

        ret = getA(p, 0, 1)        
        posts = ret['response'][0]
        print 'posts = ' + str(posts)

        steps = ret['response'][0]/100 + 1

        output = []
        i = 0
        j = sss = 1
        end = 100
        for i in range(0, steps):
            if posts > end:
                posts -= end
            else:
                end = posts

            ret = getA(p, i*100, end)
            for j in range(1, end+1):
                try:
                    l = 'vk.com/'+p+'?w=wall'+str(ret['response'][j]['from_id']) + '_' + str(ret['response'][j]['id'])
                    output.append({'link': l, 'comm': ret['response'][j]['comments']['count'], 'like': ret['response'][j]['likes']['count'], 'repo': ret['response'][j]['reposts']['count']})
                except:
                    pass

        output.sort(key=lambda x: x['like'], reverse=True) #sort by key 

        g = open(p + '.txt', 'a')
        for item in output:
            g.write('\n<tr align="center">\n<td>'+ str(a[i][0]) +\
                    '</td>\n<td>'+str(a[i][2])+\
                    '</td>\n<td>'+str(a[i][3])+\
                    '</td>\n<td><a href="https://'+a[i][1]+\
                    '" target="_blank">Check it' +\
                    '</a></td>\n</tr>')            
        g.write('</table>\n<br><div align="center"><a href="https://github.com/d3QUone/vk-analytics2" target="_blank">Follow me on GitHub!</a></div><br>\n</body>\n</html>')
        g.close()
        inp = f.readline()

    f.close
    print '\nDone.'
    

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
    response = urllib.urlopen('https://api.vk.com/method/wall.get?domain=' + dom + '&offset=' + str(off) +'&count=' + str(cou))
    return json.load(response)
                              
main()
