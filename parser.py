f = open("lineup.txt","r")
o = open("adjustedlineup.txt","w")

def washington():
    out = u''
    for i, line in enumerate(f.readlines()):
        if i%3 != 2:
            out += line.strip().encode('utf8') + u' '
        else:
            o.write(out.encode('utf8')+u'\n')
            out = u''

def washcal():
    for i, line in enumerate(f.readlines()):
        o.write((line.split(' ')[2]+u' '+line.split(' ')[3]+u'\n').encode('utf8'))

def windermere():
    for i, line in enumerate(f.readlines()):
        if i%2 == 1:
            line = line.strip()
            o.write((line.split(' ')[0]+u' '+line.split(' ')[1]+u'\n').encode('utf8'))
            
washington()
f.close()
o.close()
