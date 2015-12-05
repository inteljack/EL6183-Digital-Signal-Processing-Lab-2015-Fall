import sys; files = [sys.stdout]; map(         # unpack (right?...)
     lambda line:
         (line[:6] != "::::::" and [files[-1].write(line)])
          or files.append( open(line[6:-1],'w') ),
     sys.stdin.readlines())
