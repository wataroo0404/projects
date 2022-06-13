from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

#matplotlib inline  

import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import imageio
from tqdm import tqdm_notebook as tqdm

print('Version information')

print('python: {}'.format(sys.version))
print('matplotlib: {}'.format(matplotlib.__version__))
print('numpy: {}'.format(np.__version__))


def pairwise_dist(x, y):
    # x[None,:] outputs all elements of x
    # np.sum() Sum of array elements over a given axis 1==y-axis
    # x**2 is each element squared but np.dot(x,x) is matrix multiplication
    # x[0,0] prints first element in first array row
    dist = np.sum((x[None, :] - y[:, None]) **2, -1 )**0.5
    dist = np.transpose(dist)
    return dist

    raise NotImplementedError

def softmax(logits):
    #raise NotImplementedError
    #need to subtract the maximum for each row of logits
    logits = logits - np.expand_dims(np.max(logits,1), 1)
    logits = np.exp(logits)
    axis_sum = np.expand_dims(np.sum(logits, 1),1)
    p = logits / axis_sum
    return p

def logsumexp(logits):
	#get the number of rows in input matrix
	i = logits.shape[0]
	#handle over and underflow
	logits = np.rollaxis(logits, 1)
	vmax = logits.max(axis=0)
	out = np.log(np.sum(np.exp(logits - vmax), axis=0))
	out += vmax
	out = out.reshape(i,1)
	return out


# below are some helper functions for plot.
# you don't have to modify them. 

def plot_images(img_list, title_list, figsize=(11, 6)):
    assert len(img_list) == len(title_list)
    fig, axes = plt.subplots(1, len(title_list), figsize=figsize)
    for i, ax in enumerate(axes):
        ax.imshow(img_list[i] / 255.0)
        ax.set_title(title_list[i])
        ax.axis('off')

def plot_scatter(samples, ids):
    colors = np.zeros((len(ids), 3))
    choices = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    num_points = []
    for i in range(3):
        num_points.append(np.sum(ids == i))
    maps = np.argsort(num_points)
    for i in range(3):
        colors[np.where(ids == maps[i]), :] = choices[i]
    plt.scatter(samples[:, 0], samples[:, 1], s=1, color=colors)
    plt.axis('equal')





class KMeans(object):

    def __init__(self):
    	pass


    def _init_centers(self, points, K, **kwargs):

        """
        Args:
            points: NxD numpy array, where N is # points and D is the dimensionality
            K: number of clusters
            kwargs: any additional arguments you want
        Return:
            centers: ? x D numpy array, the centers. Note that it is possible that we just need fewer centers.
            (e.g., 1 cluster is enough when all the points are the same). 
        """
        # points.shape[0] gives number of points i.e. # of columns
        # index point matrix with random index, select k random points 
        centers = points[np.random.randint(points.shape[0], size= K)]

        return centers

    def _update_assignment(self, centers, points):
        """
        Args:
            centers: KxD numpy array, where K is the number of clusters, and D is the dimension
            points: NxD numpy array, the observations
        Return:
            cluster_idx: numpy array of length N, the cluster assignment for each point
        """
        #distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
        distances = pairwise_dist(centers, points)
        cluster_idx = np.argmin(distances, axis=0)
        return cluster_idx

    def _update_centers(self, old_centers, cluster_idx, points):
    	centers = np.empty((0, points.shape[1]))
    	for i in range(old_centers.shape[0]):
    		add = np.array(points[cluster_idx == i, :].mean(axis=0))
    		centers = np.append(centers, [add], axis=0)

    	return centers


    def _get_loss(self, centers, cluster_idx, points):
        """
        Args:
            centers: KxD numpy array, where K is the number of clusters, and D is the dimension
            cluster_idx: numpy array of length N, the cluster assignment for each point
            points: NxD numpy array, the observations
        Return:
            loss: a single float number, which is the objective function of KMeans.
        """
        raise NotImplementedError
        
    def __call__(self, points, K, max_iters=100, abs_tol=1e-16, rel_tol=1e-16, **kwargs):
        """
        Args:
            points: NxD numpy array, where N is # points and D is the dimensionality
            K: number of clusters
            max_iters: maximum number of iterations
            abs_tol: convergence criteria w.r.t absolute change of loss
            rel_tol: convergence criteria w.r.t relative change of loss
            kwargs: any additional arguments you want
        Return:
            cluster assignments: Nx1 int numpy array
            cluster centers: ? x D numpy array, the centers
        """
        centers = self._init_centers(points, K, **kwargs)
        pbar = tqdm(range(max_iters))
        for it in pbar:
            cluster_idx = self._update_assignment(centers, points)
            centers = self._update_centers(centers, cluster_idx, points)
            loss = self._get_loss(centers, cluster_idx, points)
            K = centers.shape[0]
            if it:
                diff = np.abs(prev_loss - loss)
                if diff < abs_tol and diff / prev_loss < rel_tol:
                    break
            prev_loss = loss
            pbar.set_description('iter %d, loss: %.4f' % (it, loss))
        return cluster_idx, centers



#--------------------kmeans tester -----------------------------
image = imageio.imread('gatech.bmp')
im_height, im_width, im_channel = image.shape
flat_img = np.reshape(image, [-1, im_channel]).astype(np.float32)
cluster_ids, centers = KMeans()(flat_img, K=5)
kmeans_img = np.reshape(centers[cluster_ids], (im_height, im_width, im_channel))
plot_images([image, kmeans_img], ['origin', 'kmeans'])




#points = np.array([[0,1], [2,3], [4,5]])
#k = KMeans()
#centers = k._init_centers(points, 3)
#print(centers)
#print()
#update = k._update_assignment(centers, points)
#print(update)
#print()
#new_center = k._update_centers(centers,update,points)
#print(new_center)
#