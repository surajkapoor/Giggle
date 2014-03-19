import pdb

def main():
    low = 0
    high = 1
    for i in range(10):
        pdb.set_trace()
        new_high = get_new_high(low, high)
        low = high
        high = new_high

def get_new_high(low, high):
    return low + high

if __name__ == '__main__':
    main()