import threading
import threader

lock = threading.Lock()
t1 = threader.PingTread(lock)
t1.setDaemon(True)
t1.start()