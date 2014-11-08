# sort by num of posts
import urllib, json

def main():  
    try:
        f = open('_input.txt', 'r')
        data = f.read()
        f.close()
    except:
        f = open('_input.txt', 'w+')
        f.close()
        print 'No input file'
        exit()
    data = data.split('\n')
    #print data

    buf = []
    for link in data:
        #make req
        try:
            L = link.replace('\n', '').split('/')
            dom = L[len(L)-1]
            ret = getA(dom, off=0, cou=1)
            count = ret['response']['count']
            buf.append({"link":link, "count":count})
        except BaseException as ex:
            print ex

    # sort that
    output = [[o["count"], o["link"]] for o in buf]
    output.sort(reverse=True)
    print output
    
    # save now
    f = open('_input.txt', 'w+')
    for item in output:
        f.write(item[1] + '\n')
    f.close()
    print 'Done'
    
    

def getA(dom, off=0, cou=100):
    response = urllib.urlopen('https://api.vk.com/method/wall.get?domain='+dom+\
                              '&offset='+str(off)+'&count=' + str(cou) + '&v=5.26')
    return json.load(response)
                              

main()
