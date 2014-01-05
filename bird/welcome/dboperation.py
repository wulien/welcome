from models import WaitForVerify, OnLine, HistoryInfo

class db(object):

    #operation for table WaitForVerify
    def SaveToTable_WaitForVerify(self, ip, phone_no, random_no):
        table = WaitForVerify()
        table.ip = ip
        table.phone_no = phone_no
        table.random_no = random_no
        table.save()

    def check_verify_no(self, verify_no, phone_no):
        try:
            p = WaitForVerify.objects.get(random_no=verify_no)
        except WaitForVerify.DoesNotExist:
            return False
        if p.phone_no != phone_no:
            return False
        return True

    #operation for table OnLine
    def SaveToTable_OnLine(self, ip, phone_no):
        table = OnLine()
        table.ip = ip
        table.phone_no = phone_no
        table.save()

    def check_phone_online(self, phone):
        try:
            OnLine.objects.get(phone_no=phone)
        except OnLine.DoesNotExist:
            return False
        return True

    #operation for table HistoryInfo
    def SaveToTable_HistoryInfo(self, phone_no):
        table = HistoryInfo()
        table.phone_no = phone_no
        table.save()

