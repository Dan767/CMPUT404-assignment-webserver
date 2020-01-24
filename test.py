import os

def list_dir(dir_name, traversed = [], results = []): 
    dirs = os.listdir(dir_name)
    results.append(dir_name)
    if dirs:
        for f in dirs:
            new_dir = dir_name + f + '/'
            if os.path.isdir(new_dir) and new_dir not in traversed:
                traversed.append(new_dir)
                list_dir(new_dir, traversed, results)
            else:
                results.append(new_dir[:-1])  
    return results

dirs = list_dir('www/')
print(dirs)

req = 'www/hardcode/'

reqs = [x for x in dirs if req in x and x != req]
reqs = [x for x in reqs if (x.count('/')==req.count('/') or (x.count('/')==(req.count('/')+1) and x[-1] == '/'))]
reqs = [x[len(req)-1:] for x in reqs]
print(reqs)