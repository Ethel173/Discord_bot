import random
import sys

def roll_random_in_array(rng_array,seed_val=0):
    if seed_val != 0:
        random.seed(seed_val)
    #need -1 since index starts at 0 but len starts at 1
    i = random.randint(0,len(rng_array)-1)
    return rng_array[i]

def psudo_list_rng(list_a,str_t):
    res = [i for i in list_a if str_t not in i]
    return res

if __name__ == "__main__":
    sys.exit(1)
