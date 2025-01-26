def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        if arr[mid] < target:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1

    if upper_bound is None:
        if low < len(arr):
            upper_bound = arr[low]

    return (iterations, upper_bound)

sorted_array = [0.5, 1.2, 2.3, 3.5, 3.6, 3.7, 4.0, 5.9, 6.3, 6.7,]

target_value = 4.5
result = binary_search(sorted_array, target_value)
print(result)
