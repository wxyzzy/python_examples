# example of creating and deleting objects
# if there are non-Python resources that must be deleted.

class ObjectCount:
    count = 0
    def __init__(self):
        ObjectCount.count += 1
        print(f"Instantiate object; count = {ObjectCount.count}")
    def __del__(self):
        ObjectCount.count -= 1
        print(f"Destroy object; count = {ObjectCount.count}")
