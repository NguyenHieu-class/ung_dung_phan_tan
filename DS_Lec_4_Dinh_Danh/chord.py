#Chord DHT implementation in Python
from pprint import pprint

def binarySearch(alist, item):                                                                                                    # Tìm kiếm nhị phân trong mảng đã sắp xếp
    first = 0
    last = len(alist)-1
    found = False
    
    while first<=last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    
    return found, midpoint

def successor(L, n):                                                                                                                # Tìm node kế tiếp của n trong ring, nếu n không tồn tại thì trả về None
    found, midpoint = binarySearch(L,n)
    if L[midpoint] >= n:
        return L[midpoint]
    if L[midpoint] < n:
        if midpoint==len(L)-1:
            return None
        return L[midpoint+1]


def get_fingers(nodes, m):                                                                                                        # Tạo bảng finger cho mỗi node trong ring
    nodes_augment = nodes.copy()
    nodes_augment = sorted(nodes_augment)
    maxnum = pow(2,m)
    nodes_augment.append(nodes_augment[0]+maxnum)
    
    finger_table = {}
    for node in nodes: 
        fingers = [None]*m
        for i in range(m):
            j = (node + pow(2,i))%maxnum
            fingers[i] = successor(nodes_augment,j)%maxnum
        finger_table[node] = fingers.copy()
        
    return finger_table

def get_key_loc(nodes, k, m):                                                                                                    # Tìm vị trí của key k trong ring
    nodes_augment = nodes.copy()
    nodes_augment = sorted(nodes_augment)
    maxnum = pow(2,m)
    nodes_augment.append(nodes_augment[0]+maxnum)
    return successor(nodes_augment, k)%maxnum


def get_query_path(nodes, k, n, m):                                                                                             # Tìm đường đi từ node n đến vị trí của key k
    nodes_copy = nodes.copy()
    nodes_copy = sorted(nodes_copy)
    
    k_loc = get_key_loc(nodes_copy, k, m)
    fingers = get_fingers(nodes_copy, m)
    query_path = [n]
    
    while(True):
        
        if k_loc==n:
            return query_path

        f = fingers[n]
        
        i = 0
        x = f[i]
        
        if k_loc > n: 
            while (x < k_loc) and (x > n):
                i += 1
                if i == len(f):
                    break
                x = f[i]
                
        if k_loc < n: 
            while ( ((x > k_loc) and (x > n)) or ((x < k_loc) and (x < n)) ):
                i += 1
                if i == len(f):
                    break
                x = f[i]
        if i==0:
            n = f[0]
        else:
            n = f[i-1]
            
        query_path.append(n)
    
if __name__=="__main__":                                                                                                            # Test
    
    nodes = [112, 96, 80, 16, 32, 45] # nodes in the P2P system
    m = 7 # Ring is of size 2^m
    print('Chord DHT with peers {nodes}, and m = {m} \n'.format(nodes=nodes, m=7))
    
    print('The finger table for this DHT is: ')
    pprint(get_fingers(nodes, m))
    print()
    
    file_key = 42
    print('File location for file key {file_key} is at node {file_key_location} \n'.format(
        file_key=file_key, file_key_location=get_key_loc(nodes, file_key, m)
    ))
    query_node = 80
    print('Query path for file {file_key} with origin node {query_node} : {query_path}'.format(
        file_key=file_key, query_node=query_node, query_path=get_query_path(nodes, file_key, query_node, m)
    ))
    query_node = 96
    print('Query path for file {file_key} with origin node {query_node} : {query_path}'.format(
        file_key=file_key, query_node=query_node, query_path=get_query_path(nodes, file_key, query_node, m)
    ))
    query_node = 45
    print('Query path for file {file_key} with origin node {query_node} : {query_path}'.format(
        file_key=file_key, query_node=query_node, query_path=get_query_path(nodes, file_key, query_node, m)
    ))