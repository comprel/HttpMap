import IPy


def getRequestIpaddress(req):
    try:
        return req.remote_addr
    except:
        return ""


def is_ip(ipaddress):
    try:
        IPy.IP(ipaddress)
        _point = ipaddress.split(".")
        if len(_point) != 4:
            return False
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    print(is_ip("127.0.0.1"))
