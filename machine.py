import random
from itertools import combinations
from shapely.geometry import LineString, Point

class MACHINE():
    """
        [ MACHINE ]
        MinMax Algorithm을 통해 수를 선택하는 객체.
        - 모든 Machine Turn마다 변수들이 업데이트 됨

        ** To Do **
        MinMax Algorithm을 이용하여 최적의 수를 찾는 알고리즘 생성
           - class 내에 함수를 추가할 수 있음
           - 최종 결과는 find_best_selection을 통해 Line 형태로 도출
               * Line: [(x1, y1), (x2, y2)] -> MACHINE class에서는 x값이 작은 점이 항상 왼쪽에 위치할 필요는 없음 (System이 organize 함)
    """
    def __init__(self, score=[0, 0], drawn_lines=[], whole_lines=[], whole_points=[], location=[]):
        self.id = "MACHINE"
        self.score = [0, 0] # USER, MACHINE
        self.drawn_lines = [] # Drawn Lines
        self.board_size = 7 # 7 x 7 Matrix
        self.num_dots = 0
        self.whole_points = []
        self.location = []
        self.triangles = [] # [(a, b), (c, d), (e, f)]

    def find_best_selection(self):
        # (1) 짝수 개의 삼각형 탐색
        line = self.find_even_triangle_strategy()
        if line:
            return line
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
        return random.choice(available)
    
    def check_availability(self, line):
        line_string = LineString(line)

        # Must be one of the whole points
        condition1 = (line[0] in self.whole_points) and (line[1] in self.whole_points)
        
        # Must not skip a dot
        condition2 = True
        for point in self.whole_points:
            if point==line[0] or point==line[1]:
                continue
            else:
                if bool(line_string.intersection(Point(point))):
                    condition2 = False

        # Must not cross another line
        condition3 = True
        for l in self.drawn_lines:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in self.drawn_lines)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    
    
    # (2) 

    def find_even_triangle_strategy(self):
    # 삼각형 탐색
        for line in self.drawn_lines:
            connected_lines = self.find_connected_lines(line)
            for connected_line in connected_lines:
                # 삼각형 확인
                possible_triangle = self.form_triangle(line, connected_line)
                if possible_triangle and self.is_triangle_empty(possible_triangle):
                    # 삼각형 내부에 다른 점이 없는지 확인
                    if self.can_form_even_number_of_triangles(possible_triangle):
                        # 짝수 균형을 유지할 수 있는 선분 찾기
                        return self.select_line_to_maintain_even_balance(possible_triangle)
        return None

    def find_connected_lines(self, line):
        # 주어진 선분과 연결된 다른 선분들을 찾는 함수
        connected = []
        for other_line in self.drawn_lines:
            if line != other_line and (line[0] in other_line or line[1] in other_line):
                connected.append(other_line)
        return connected

    def form_triangle(self, line1, line2):
        # 주어진 두 선분으로 삼각형을 형성할 수 있는지 확인하는 함수
        points = set(line1 + line2)
        if len(points) == 3:
            return list(points)
        return None
        
    def is_triangle_empty(self, triangle):
        # 주어진 삼각형 내부에 다른 점이 없는지 확인하는 함수
        triangle_set = set(triangle)
        for point in self.whole_points:
            if point not in triangle_set:
                if self.is_point_inside_triangle(point, triangle):
                    return False
        return True

    def is_point_inside_triangle(self, point, triangle):
        # 삼각형 내부에 점이 있는지 판별하는 로직
        pass 

    def can_form_even_number_of_triangles(self, triangle):
        # 주어진 삼각형을 완성하였을 때 짝수 개의 삼각형을 유지할 수 있는지 확인하는 함수
        pass

    def select_line_to_maintain_even_balance(self, triangle):
        # 짝수 균형을 유지할 수 있는 선분을 선택하는 함수
        pass

    def find_available_lines(self):
        # 사용 가능한 모든 선분을 찾는 함수
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
        return available
