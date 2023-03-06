import random


def createSessionIdForCookie(size: int) -> str:
    possibilities = "AZERTYUIOPQMSLDKFJGHNWBXVCazertyuiopqsdfghjklmwxcvbn123456789*!$&."

    sessionId = ""
    for i in range(size):
        sessionId += possibilities[random.randint(0, len(possibilities)-1)]
    
    return sessionId


# if __name__ == '__main__':
#     print(createSessionIdForCookie(455))