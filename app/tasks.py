from time import sleep
def example(seconds):
    print('starting task')
    for i in range(seconds):
        print(i)
        sleep(1)
    print('task completed')

if __name__ == '__main__':
    example(3)