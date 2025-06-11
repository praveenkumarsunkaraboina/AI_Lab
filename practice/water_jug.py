import heapq
import math
from collections import deque

def water_jug_ucs(a,b,d):
    if d>max(a,b) or d%math.gcd(a,b)!=0:
        return -1,[]
    pq=[(0,0,0,[])]
    vis=set()
    while pq:
        cost, jugA, jugB, path=heapq.heappop(pq)
        new_path=path+[(jugA, jugB)]

        if jugA==d or jugB==d:
            return cost, new_path
        
        if (jugA, jugB) in vis:
            continue
        vis.add((jugA, jugB))

        next_states=[
            (a,jugB),
            (jugA,b),
            (0,jugB),
            (jugA,0),
            (jugA+min(a-jugA,jugB),jugB-min(a-jugA,jugB)),
            (jugA-min(b-jugB,jugA),jugB+min(b-jugB,jugA))
        ]

        for state in next_states:
            heapq.heappush(pq,(cost+1,state[0],state[1],new_path))
    return -1,[]

def water_jug_dfs(a,b,d):
    if d>max(a,b) or d%math.gcd(a,b)!=0:
        return -1,[]
    stack=[(0,0,0,[])]
    vis=set()
    while stack:
        cost, jugA, jugB,path=stack.pop()
        new_path=path+[(jugA,jugB)]
        
        if jugA==d or jugB==d:
            return cost,new_path
        
        if (jugA,jugB) in vis:
            continue
        vis.add((jugA,jugB))

        next_states=[
            (a,jugB),
            (jugA,b),
            (0,jugB),
            (jugA,0),
            (jugA-min(jugA,b-jugB),jugB+min(jugA,b-jugB)),
            (jugA+min(jugB,a-jugA),jugB-min(jugB,a-jugA))
        ]

        for state in next_states:
            stack.insert(0,(cost+1,state[0],state[1],new_path))
    return -1,[]

def water_jug_bfs(a,b,d):
    if d>max(a,b) or d%math.gcd(a,b)!=0:
        return -1,[]
    
    q=deque()
    q.append((0,0,0,[]))
    vis=set()
    while q:
        cost, jugA, jugB,path=q.popleft()
        new_path=path+[(jugA,jugB)]
        if jugA==d or jugB==d:
            return cost, new_path
        if (jugA,jugB) in vis:
            continue
        vis.add((jugA,jugB))
        
        next_states=[
            (a,jugB),
            (jugA,b),
            (0,jugB),
            (jugA,0),
            (jugA-min(jugA,b-jugB),jugB+min(jugA,b-jugB)),
            (jugA+min(jugB,a-jugA),jugB-min(jugB,a-jugA))
        ]

        for state in next_states:
            q.append((cost+1,state[0],state[1],new_path))
    
    return -1,[]
        


def main():
    a=int(input("Enter the capacity of jugA:"))
    b=int(input("Enter the capacity of jugB:"))
    d=int(input("Enter the target capacity:"))

    result, path=water_jug_dfs(a,b,d)
    if result==-1:
        print("No solution found!!")
    
    else:
        print(f"Minimum number of steps: {result}\n")
        print("Solution path:")
        for state in path:
            print(f"({state[0]},{state[1]})")

if __name__=="__main__":
    main()