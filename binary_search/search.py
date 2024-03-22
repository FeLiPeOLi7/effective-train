
def binary_search(arr, x):
    first = 0
    last = len(arr) - 1
    mid = 0

    while first <= last:
        mid = (first + last) // 2
        if arr[mid] < x:
            first = mid + 1
        elif arr[mid] > x:
            last = mid - 1
        else:
            return mid
    return -1

arr = range(10)
x = int(input("Put your x: "))

result = binary_search(arr, x)

if result != -1:
    print("Element is present at index", str(result))
else:
    print("Element is not present in array")

