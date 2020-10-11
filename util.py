def listtostr(list,sep):
    re=""
    for i in list:
        if re!="":
            re+=sep
        re+=i.get_text()
    return re