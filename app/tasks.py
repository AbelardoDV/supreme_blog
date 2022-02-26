from time import sleep
from rq import get_current_job

def example(seconds):
    job = get_current_job()
    if job:
        job.meta['progress'] = 0
        print('starting task')
        for i in range(seconds):
            print(i)
            job.meta['progess'] = 100 * i / seconds
            job.save_meta()
            sleep(1)
        job.meta['progress'] = 100
        job.save_meta()
        print('task completed')

if __name__ == '__main__':
    example(3)