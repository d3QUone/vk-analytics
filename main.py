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
        g = open(p + '.txt', 'w')
        g.close
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
            g.write('like=' + str(item['like']) + ' comm='+str(item['comm'])+' repo='+str(item['repo'])+'; link: ' + item['link'] + '\n')
        g.close()
        
        print '-'*40 + '\n'
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
