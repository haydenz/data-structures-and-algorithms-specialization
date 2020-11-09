# python3

from collections import namedtuple

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])

class Heap:
    def __init__(self, data):
        self.heap = data
        self.size = len(data)
    
    def __left_child(self, i):
        if 2*(i+1) - 1 >= len(self.heap):
            return i
        else:
            return 2*(i+1) - 1

    def __right_child(self, i):
        if 2*(i+1) >= len(self.heap):
            return i
        else:
            return 2*(i+1)

    def __parent(self, i)
        if i != 0:
            return (i + i%2) / 2 - 1
        else:
            return i

    def shift_down(self, i):
        min_idx = i
        l = self.__left_child(i)
        r = self.__right_child(i)
        if l <= len(self.heap) - 1 and self.heap[l][0] < self.heap[min_idx][0]:
            min_idx = l
        if r <= len(self.heap) - 1 and self.heap[r][0] < self.heap[min_idx][0]:
            min_idx = r
        if i != min_idx:
            self.heap[i], self.heap[min_idx] = self.heap[min_idx], self.heap[i]
            self.shift_down(min_idx)
        
    def shift_up(self):
        for i in range(self.size, 0, -1):
            p = self.__parent(i)
            l = self.__left_child(p)
            r = self.__right_child(p)
            if self.heap[l][0] == self.heap[r][0]:
                if self.heap[l][1] > self.heap[r][1]:
                    self.heap[l], self.heap[r] = self.heap[r], self.heap[l]
                if self.heap[p][0] == self.heap[l][0] and self.heap[p][1] > self.heap[l][1]:
                    self.heap[l], self.heap[p] = self.heap[p], self.heap[l]
                    
            if self.heap[p][0] == self.heap[min_thread][0]:
                if self.heap[p][1] > self.heap[min_thread][1]:
                    min_thread = p


    def extract_min(self):
        return self.heap[0]

    def insert(self, insert_val):
        self.heap[0][0] = insert_val

def efficient_parallel(n_workers, jobs):
    tmp, result = [], []
    # make a heap
    for i in range(n_workers):
        tmp.append([0, i])
    heap = Heap(tmp)
    del tmp

    for i in range(len(jobs)):
        latest_time, latest_thread = heap.extract_min()
        heap.insert(latest_time + jobs[i])
        heap.shift_down(0)
        heap.swap_thread()

        result.append(AssignedJob(latest_thread, latest_time))
    return result

def assign_jobs(n_workers, jobs):
    # TODO: replace this code with a faster algorithm.
    result = []
    next_free_time = [0] * n_workers
    for job in jobs:
        next_worker = min(range(n_workers), key=lambda w: next_free_time[w])
        result.append(AssignedJob(next_worker, next_free_time[next_worker]))
        next_free_time[next_worker] += job

    return result

def main():
    # n_workers, n_jobs = map(int, input().split())
    n_workers, n_jobs = 4, 20
    # jobs = list(map(int, input().split()))
    jobs = [1] * 20
    assert len(jobs) == n_jobs

    assigned_jobs = efficient_parallel(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()
