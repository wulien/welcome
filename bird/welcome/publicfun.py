import random
import logging

def CheckPhoneNo(phone_no):
    if 11 != len(phone_no) or '1' != phone_no[0]:
        return False
    for no in phone_no:
        if no < '0' or no > '9':
            return False
    return True

def GenerateRandomNo():
    return random.randint(100, 999)

def log(strLog):
    FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        filename='bird.log',
                        filemode='w')
    logging.info(strLog)