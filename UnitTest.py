from tools.Checker import Authenticate

auth = Authenticate({
    'user':'brendanshauncaldwell@gmail.om',
    'pass':'Illumina3'
}, {
    'type':'https',
    'proxy': '158.69.64.142:9300'
})

auth.authenticate()