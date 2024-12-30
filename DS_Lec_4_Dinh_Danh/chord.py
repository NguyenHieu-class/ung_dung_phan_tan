# Chuong trinh mo phong thuat toan Chord DHT
from pprint import pprint

def binarySearch(arr, item):                                                                # Ham tim kiem nhi phan
    first = 0
    last = len(arr) - 1
    found = False
    while (first <= last and not found):
        mid = (first + last) // 2
        if arr[mid] == item:
            found = True
        else:
            if item < arr[mid]:
                last = mid - 1
            else:
                first = mid + 1
    return found, mid

def successor(L, n):                                                                        # Ham tim kiem successor
    found, mid = binarySearch(L, n)
    if L[mid] >= n:
        return L[mid]
    if L[mid] < n:
        if mid == len(L) - 1:
            return None
        return L[mid + 1]

def get_fingers(nodes, m):                                                                  # Tao bang finger
    nodes_augment = nodes.copy()
    nodes_augment = sorted(nodes_augment)
    max_node = pow(2, m)

    # wraparound first node to accommodate nodes clockwise of n when n is the larger than the largest value node
    nodes_augment.append(nodes_augment[0] + max_node)

    finger_table = {}
    for node in nodes:
        fingers = [None] * m
        for i in range(m):
            j = (node + pow(2, i)) % max_node
            fingers[i] = successor(nodes_augment, j)%max_node
        finger_table[node] = fingers.copy()
    return finger_table

def get_key_loc(nodes, k, m):                                                            # Tim vi tri cua key
    nodes_augment = nodes.copy()
    nodes_augment = sorted(nodes_augment)
    max_node = pow(2, m)

    # wraparound first node to accommodate nodes clockwise of n when n is the larger than the largest value node
    nodes_augment.append(nodes_augment[0] + max_node)
    return successor(nodes_augment, k)%max_node

def get_query_path(nodes, k, n, m):                                                      # Tim duong truy van
    nodes_copy = nodes.copy()
    nodes_copy = sorted(nodes_copy)

    # vi tri cua key
    key_loc = get_key_loc(nodes_copy, k, m)

    # finger table
    fingers = get_fingers(nodes_copy, m)

    # bat dau tim duong truy van tu node co ban
    query_path = [n]

    while (True):
        
        # return duong truy van neu tim thay key
        if key_loc == n:
            return query_path
        
        f = fingers[n]

        i=0
        x = f[i]

        if key_loc > n:
            
            # Neu duong dan clockwise nam giua node co ban vaf vi tri cua key ma khong phai 0, tat ca cac node nam giua se la duong dan truy van
            # duong dan (x) phai nam trong khoang key_loc > x > x
            while (x <= key_loc) and (x > n):
                i += 1
                if i == len(f):
                    break
                x = f[i]

        if key_loc < n:
            # Neu duong dan counter-clockwise nam giua node co ban vaf vi tri cua key ma khong phai 0, tat ca cac node nam giua se la duong dan truy van
            # duong dan (x) phai nam trong khoang (key_loc < x) && (n < x) OR (key_loc > x) && (n > x)
            while (x >= key_loc) and (x < n):
                i += 1
                if i == len(f):
                    break
                x = f[i]

        # Them node tiep theo vao duong dan truy van
        if i == 0:
            n = f[0]
        else:
            n = f[i-1]
        query_path.append(n)

if __name__ == "__main__":
    # Test case

    nodes = [143, 90, 80, 15, 31, 46]                                                      # list node
    m = 7
    print("Chord DHT: ", nodes, "m = ", m, "\n")
    print("Finger Table:\n")
    pprint(get_fingers(nodes, m))                                                          # in bang finger
    print("\n")

    key = 44                                                                               # key can tim
    print("Key location for key = ", key, "is at node: ", get_key_loc(nodes, key, m), "\n")

