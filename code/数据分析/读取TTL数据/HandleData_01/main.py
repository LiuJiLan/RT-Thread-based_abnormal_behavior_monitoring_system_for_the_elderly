from collections import deque

queList = deque()
queSum = 0
max_length = 10
min_length = 60000

def deal_with_que(que, sum, max, data):
    if len(que) < max:
        que.append(data)
        sum += data
    else:
        que.append(data)
        sum = sum + data - que.popleft()
    return sum

for i in range(20):
    queSum = deal_with_que(queList, queSum, max_length, i)
    print(queSum)
    print(queList)