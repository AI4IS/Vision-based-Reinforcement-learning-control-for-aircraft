import multiprocessing

def worker(num):
    """每个工作进程要执行的任务"""
    while True:
        print(f'Worker {num} 开始执行')
        # 在这里执行你的任务
        print(f'Worker {num} 完成')

if __name__ == '__main__':
    num_processes = 4
    processes = []

    # 创建工作进程并将其添加到进程列表中
    process1 = multiprocessing.Process(target=worker, args=(1,))
    processes.append(process1)
    process2 = multiprocessing.Process(target=worker, args=(2,))
    processes.append(process2)

    # 启动所有工作进程
    for process in processes:
        process.start()

    # 等待所有工作进程完成
    for process in processes:
        process.join()

    print('所有工作进程已完成')