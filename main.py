import time
from timeloop import Timeloop
from datetime import timedelta



tl = Timeloop()


@tl.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print("2s job current time : {}".format(time.ctime()))


if __name__ == "__main__":
    tl.start(block=False)
    time.sleep(1)
    print('Non-blocked execution')
    time.sleep(10)
    print('Non-blocked execution')
    tl.stop()
    time.sleep(10)
    print('Non-blocked execution')



