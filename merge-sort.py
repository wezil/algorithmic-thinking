"""
Simple Merge Sort algorithm for sorting 
lists

"""

def merge_sort(elements):
    """ dividing and recursive part """
    
    if len(elements) > 1:
        midpoint = len(elements) // 2
        left = list(elements[0 : midpoint])
        right = list(elements[midpoint : ])
        merge_sort(left)
        merge_sort(right)
        merge(left, right, elements)

def merge(left, right, elements):
    """ merging part """
    
    idx_i = 0
    idx_j = 0
    idx_k = 0
    
    while idx_i < len(left) and idx_j < len(right):
        if left[idx_i] <= right[idx_j]:
            elements[idx_k] = left[idx_i]
            idx_i += 1
        else:
            elements[idx_k] = right[idx_j]
            idx_j += 1
        idx_k += 1
        
    if idx_i == len(left):
        elements[idx_k:] = right[idx_j:]
    else:
        elements[idx_k:] = left[idx_i:]
