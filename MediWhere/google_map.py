
def make_googlemap_url(center ,zoom = 15):
    key = 'AIzaSyA9gjC63ldBuHDwYM6flkFJDbTq6vQhFdg'
    point = str(center[1]) +','+ str(center[0])
    size = (500,500)

    url = "http://maps.google.com/maps/api/staticmap?"
    url += "center=%s&" % point
    url += "zoom=%i&" % zoom
    url += 'scale=1&'
    url += "size=" + str(size[0]) + 'x' + str(size[1]) + '&'
    url += 'maptype=roadmap&'
    url +='&markers=color:red%7Clabel:C%7C' + point + '&'
    url += 'key=' + key

    return url