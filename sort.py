import sys

from main import FILENAME, request_data


def sort_input():  
    try:
        with open(FILENAME, "r") as f:
            data = f.read().split("\n")
        buf = []
        append = buf.append
        for link in data:
            if link == "":
                continue
            try:
                L = link.split("/")
                dom = L[len(L)-1]
                ret = request_data(dom, 0, 1)
                if "response" in ret and "count" in ret["response"]:
                    count = ret["response"]["count"]
                    append({"link": link, "count": count})
                else:
                    print "Bad response: {0}".format(ret)
            except Exception as e:
                print "Sorting exceprion: {0}".format(repr(e))
        output = [[o["count"], o["link"]] for o in buf]
        output.sort(reverse=True)
        f = open(FILENAME, "w")
        for item in output:
            f.write("{0}\n".format(item[1]))
        f.close()
        print "Done"
    except IOError:
        print "No input file"
        sys.exit()


if __name__ == "__main__":
    sort_input()
