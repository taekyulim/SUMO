import numpy as np
import pickle
import argparse
import random

with open('./route_lambda.pickle', 'rb') as f:
    lambds = pickle.load(f)

def get_traffic_volume(vertex, time):
    """
    vertex : 간선 번호(1~6)
    time : 시작 시간대(1~23)
    """
    lamd = lambds[vertex-1][time-1]
    result = np.random.poisson(lamd, 1)
    return result

def random_gen():
    rand_n1 = random.uniform(0.5, 0.7)
    rand_n2 = random.uniform(0.2, 0.3)
    rand_n3 = 1 - rand_n1 - rand_n2 # [0, 0.3] 범위에서 나옴.
    
    sorted_nums = sorted([rand_n1, rand_n2, rand_n3], reverse=True)
    return sorted_nums[0], sorted_nums[1], sorted_nums[2]

def left_straight_right(route, time):
    straight_coef, left_coef, right_coef = random_gen()
    total_traffic = get_traffic_volume(route, time)
    straight = int(straight_coef*total_traffic)
    left = int(left_coef*total_traffic)
    right = int(right_coef*total_traffic)
    
    return straight, left, right

def main():
    parser = argparse.ArgumentParser(description="Get Traffic Volume in specific route and time")
    parser.add_argument('vertex', type=int, help='Vertex number 1~6')
    parser.add_argument('time', type=int, help = "Specific Time 1~23")
    
    args = parser.parse_args()
    
    result = get_traffic_volume(args.vertex, args.time)
    print(result)
    
    
if __name__ == "__main__":
    a, b, c = left_straight_right(3, 16)
    print(a, b, c)