import sys

from main import FILENAME, getInfo

def sort_input():  
    try:
        f = open(FILENAME, "r")
        data = f.read().split('\n')
        f.close()
        
        # network here..
        buf = []
        append = buf.append
        for link in data:
            try:
                L = link.replace("\n", "").split("/")
                dom = L[len(L)-1]
                ret = getInfo(dom, 0, 1)
                count = ret["response"]["count"]
                append({"link": link, "count": count})
            except BaseException as ex:
                print ex

        # sort that
        output = [[o["count"], o["link"]] for o in buf]
        output.sort(reverse=True)
        
        # save now
        f = open(FILENAME, "w+")
        for item in output:
            f.write(item[1] + '\n')
        f.close()
        print "Done"
    except IOError:
        print "No input file"
        sys.exit()
    
        

if __name__ == "__main__":
    sort_input()
