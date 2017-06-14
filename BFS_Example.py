
allPts = []
for i in range(0, IMGSIZE):
	for j in range(0, IMGSIZE):
		allPts.append((i, j))


def addNeighbors(img, points):
	neighbors = []
	for point in points:
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				if img[i, j]==0 and (i, j) in allPts:
					neighbors.append((i, j))
	return neighbors


def bfs(circles, image[][]):
	neighbors = []
	nextNeighbors[]
	for circle in circles:
		Add all points along edge to neighbors

	done = False
	curr = 1
	while not done:
		mark all points in neighbors as curr in image
		add all (points == 0, points within image boundries) neighboring neighbors to nextNeighbors
			nextNeighbors = nextNeighbors + addNeighbors(img, neighbors)
		neighbors = nextNeighbors
		nextNeighbors = []
		if len(neighbors) == 0:
			done == True
		curr += 1

def shade(img):
	minShade, maxShade = 1, max(img)
	ratio = 255/(maxShade - minShade)
	for point in image:
		image(point) = image(point) * ratio













