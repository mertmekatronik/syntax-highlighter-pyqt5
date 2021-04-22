def parse(css:str) -> dict:
    res = dict()
    for i in css.split(";"):
        if i.strip() != "":
            try: res[i.split(":")[0]] = i.split(":")[1] 
            except: pass
    return res


        
