UniDAX_APIKEY = ''
UniDAX_SECRET = ''
UniDAX_unidax_url = ''

def set(envo):
    global UniDAX_APIKEY
    global UniDAX_SECRET
    global UniDAX_unidax_url
    if envo == 'Test':
        # test 机器人
        UniDAX_APIKEY = '8595327a8947cf06492285588d761e01'
        UniDAX_SECRET = 'b2a9019765c0a64cc54214581c7366cd'
        UniDAX_unidax_url = "https://testwww.unidax.com/exchange-open-api"

    elif envo == 'Official':
        # 正式-机器人
        UniDAX_APIKEY = '8595327a8947cf06492285588d761e01'
        UniDAX_SECRET = 'b2a9019765c0a64cc54214581c7366cd'
        UniDAX_unidax_url = "https://api.unidax.com/exchange-open-api"

        # test3
        # UniDAX_APIKEY = 'dda9ce84c9e92c4703cc5fb7ab66297a'
        # UniDAX_SECRET = '01bad22db68c4e77fa4e59a4f51348e6'
        # UniDAX_unidax_url = "https://api.unidax.com/exchange-open-api"