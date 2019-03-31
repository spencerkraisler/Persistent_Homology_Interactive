import cv2
import numpy as np 
from numpy.linalg import norm

HEIGHT, WIDTH = 600, 800

# inits a black image
def create_canvas():
    canvas = np.zeros((HEIGHT, WIDTH, 3))
    return canvas.astype('uint8')

# returns a given number of points sampled from a given 2D uniform distribution
def get_points_uniform(num_of_points, xmin, xmax, ymin, ymax):
    # Args:
        # num_of_points (int): number of desired points
        # xmin, xmax (int): boundaries on x-axis
        # ymin, ymax (int): boundaries on y-axis
    X = np.random.uniform(xmin, xmax, num_of_points).astype('uint16')
    Y = np.random.uniform(ymin, ymax, num_of_points).astype('uint16')
    points = np.array([X,Y])
    points = np.reshape(points, (num_of_points, 2))
    return points

# returns a given number of points sampled from a 2D uniform distribution that
# intersects a given torus (2D torus?)
# NOTE: may not return the given number of points, since it cuts any that go 
# off the image
def get_points_torus(num_of_points, center, r1, r2):
    # Args:
        # num_of_points (int): number of points sampled
        # center (int, int): center of the torus
        # r1 (int): inner radius of torus
        # r2 (int): outer radius of torus
    points = []
    R = np.random.uniform(r1, r2, num_of_points)
    A = np.random.uniform(0, 2 * np.pi, num_of_points)
    points = [(R[i] * np.cos(A[i]) + center[0], R[i] * np.sin(A[i]) + center[1]) 
                                    for i in range(num_of_points) 
                                    if R[i] * np.cos(A[i]) + center[0] > 0 
                                    and R[i] * np.sin(A[i]) + center[1] > 0]
    points = np.array(points).astype('int16')
    return points

# draws the given points on an given color image
def draw_points(img, points):
    for pt in points:
        cv2.circle(img, (pt[0], pt[1]), 3, (0,0,255), -1)

# draws halos on a given image around given points of a selected diameter
def draw_halos(img, points, diameter):
    r = diameter // 2
    for pt in points:
        cv2.circle(img, (pt[0], pt[1]), r, (0,255,0), 1)

# returns an array of pairs of points (edges) if the points are within a 
# given diameter
def get_edges(points, diameter):
    num_of_points = points.shape[0]
    edges = [(points[i], points[j]) for i in range(num_of_points) 
                                    for j in range(num_of_points) if i != j 
                                    and norm(points[i] - points[j]) <= diameter]
    edges = np.array(edges)
    return edges

# draws the given edges on a given image
def draw_edges(img, edges):
    for edge in edges:
        cv2.line(img, tuple(edge[0]), tuple(edge[1]), (255,255,0), 2)

# for trackbar
def nothing(x):
    pass

cv2.namedWindow('image')
cv2.createTrackbar('diameter', 'image', 0, 200, nothing)
#points = get_points_uniform(50, 50, 750, 50, 550) # uniform dist.
points = get_points_torus(100, (WIDTH / 2, HEIGHT / 2), 100, 200) # torus dist.


while(True):
    canvas = create_canvas()
    diameter = cv2.getTrackbarPos('diameter','image')
    edges = get_edges(points, diameter)
    draw_edges(canvas, edges)
    draw_halos(canvas, points, diameter)
    draw_points(canvas, points)
    cv2.imshow("image", canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
