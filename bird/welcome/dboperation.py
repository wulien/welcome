import models

class db(object):

    def SetTable_WaitForVerify(self, ip, phone_no, random_no):
        table = models.WaitForVerify()
        table.ip = ip
        table.phone_no = phone_no
        table.random_no = random_no
        table.save()