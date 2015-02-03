import urllib, json, sys
from datetime import datetime

def main():
    t = datetime.now()
    try:
        f = open('input.txt', 'r')
        inp = f.readline()
        f.close()
    except:
        print "No input file"
        sys.exit(2)
    
    i = 0    
    while inp != '':
        out = 'L' + str(i) + ' '
        ret = getA(parse(inp)) 
        try:
            out += datetime.fromtimestamp(ret['response'][0]['date']).strftime('%Y-%m-%d %H:%M:%S')
            out += ': comm='+str(ret['response'][0]['comments']['count'])
            out += ', like='+str(ret['response'][0]['likes']['count'])
            out += ', reps='+str(ret['response'][0]['reposts']['count'])
        except:
            out += 'Post was deleted'
        try:
            g = open('out.txt', 'a')
        except:
            g = open('out.txt', 'w')
        g.write(out + '\n')
        g.close()
        inp = f.readline()
        i += 1

    print '\nDone\nprocessing time', datetime.now() - t, "; total processed", i+1, "links"


# parse post id 
def parse(st):
    i = start = 0
    end = len(st)
    out = '-'
    for i in range(end):
        if start == 0 and st[i] == '-':
            start = 1    
        if start == 1 and st[i].isdigit() == True: 
            out += st[i]    
        if start == 1 and st[i] == '_':
            out += st[i]   
    return out


# send request
def getA(ids):
    link = 'https://api.vk.com/method/wall.getById?posts=' + ids
    response = urllib.urlopen(link)
    r_response = json.load(response)
    return r_response
                              

main()
