import sys
from datetime import datetime
import requests

def main():
    t = datetime.now()
    try:
        f = open("input.txt", "r")
        inp = f.readline()
    except IOError:
        print "No input file"
        sys.exit()
    
    i = 0    
    while inp != "":
        ret = getA(parse(inp)) 
        try:
            out = "L{0} {1}: comm={2}, like={3}, reps={4}\n".format(
                    i, 
                    datetime.fromtimestamp(ret["response"][0]["date"]).strftime("%Y-%m-%d %H:%M:%S"),
                    ret["response"][0]["comments"]["count"],
                    ret["response"][0]["likes"]["count"],
                    ret["response"][0]["reposts"]["count"]
                )
        except IndexError:
            out = "Post was deleted\n"
        try:
            g = open('out.txt', 'a')
        except IOError:
            g = open('out.txt', 'w')
        g.write(out)
        g.close()
        inp = f.readline()
        i += 1
    f.close()
    print "Done\nProcessing time {0}; total processed {1} links".format(datetime.now() - t, i + 1)


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
def getA(posts):
    params = {
        "posts": posts,
        "v": "5.26"
    }
    r = requests.get("https://api.vk.com/method/wall.getById", params=params)
    return r.json()

                         
if __name__ == "__main__":
    main()
