from urllib.request import urlopen #For querying API
import json #For parsing API response

def GetUserScores(name, mode=0):
    print('Retrieving scores for %s' % name)
    APIKey = ReadFile('API Key.txt')
    if APIKey == '' or APIKey == ' ':
        print('No API key has been provided.')
        quit()
    response = urlopen('https://osu.ppy.sh/api/get_user_best?k=%s&m=%s&u=%s&limit=100' % (APIKey, mode, name))
    response = response.read().decode('UTF-8')
    response = json.loads(response)
    return response

def ReadFile(name):
    h = open(name, 'r')
    txt = h.read()
    h.close()
    return txt

def CalculateWeights(p):
    pps = sorted(p, reverse = True)
    totalpp = 0
    for i, pp in enumerate(pps):
        #pp weighting formula as listed here: https://osu.ppy.sh/wiki/Performance_Points
        totalpp += pp*0.95**i
    return totalpp

def main():
    users = ReadFile('users.txt')
    users = users.split('\n')
    pps = []
    for user in users:
        scores = GetUserScores(user)
        for score in scores:
            pps.append(float(score['pp']))
    total = CalculateWeights(pps)
    if len(users) > 1:
        for i, user in enumerate(users):
            if i<len(users)-1:
                print('%s, ' % user, end='')
            else:
                print('and %s would have %0.2f pp together' % (user, total))
    else:
        print('%s would have %0.2f pp' % (user, total))

if __name__ == '__main__':
    main()
