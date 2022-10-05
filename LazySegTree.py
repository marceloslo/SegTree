
class lazySegNode:
    def __init__(self, leftbound, rightbound, sum, minimum):
        self.leftbound = leftbound
        self.rightbound = rightbound
        self.minimum = minimum
        self.sum = sum
        self.left = None
        self.right = None
        self.lazy = 0
        
class LazySegTree:
    def __init__(self, array):
        self.root = self.construct(array,0,len(array)-1)
        self.array = array

    def construct(self,array,leftbound,rightbound):
        if(leftbound == rightbound):
            return lazySegNode(leftbound, rightbound, array[leftbound], array[leftbound])
        no = lazySegNode(leftbound, rightbound, -1, -1)
        sep = (leftbound + rightbound)//2 
        no.left =self.construct(array,leftbound,sep)
        no.right = self.construct(array,sep+1,rightbound)
        no.minimum = min(no.left.minimum, no.right.minimum)
        no.sum = no.left.sum + no.right.sum
        return no
    
    def queryMin(self, leftbound, rightbound):
        return self.__findMin(leftbound, rightbound, self.root)
    
    def querySum(self, leftbound, rightbound):
        return self.__findSum(leftbound, rightbound, self.root)

    def update(self,leftbound,rightbound,value):
         self.__update(leftbound,rightbound,self.root,value)

    def __findMin(self, leftbound, rightbound, node):
        #lazy propagate
        if node.lazy:
            node.sum += (node.rightbound-node.leftbound +1)*node.lazy
            node.minimum += node.lazy
            if node.leftbound != node.rightbound:
                node.left.lazy = node.lazy
                node.right.lazy = node.lazy
            else:
                self.array[node.leftbound] += node.lazy
            node.lazy = 0

        if leftbound == node.leftbound and rightbound == node.rightbound:
            return node.minimum
        mid = (node.leftbound + node.rightbound)//2
        min_left = float("inf")
        min_right = float("inf")
        if leftbound <= mid:
            min_left = self.__findMin(leftbound, min(mid,rightbound), node.left)
        if rightbound > mid:
            min_right = self.__findMin(max(leftbound, mid+1), rightbound, node.right)
        return min(min_left, min_right)

    def __findSum(self, leftbound, rightbound, node):
        #lazy propagate
        if node.lazy:
            node.sum += (node.rightbound-node.leftbound +1)*node.lazy
            node.minimum += node.lazy
            if node.leftbound != node.rightbound:
                node.left.lazy = node.lazy
                node.right.lazy = node.lazy
            else:
                self.array[node.leftbound] += node.lazy
            node.lazy = 0
        
        if leftbound == node.leftbound and rightbound == node.rightbound:
            return node.sum
        mid = (node.leftbound + node.rightbound)//2
        sum_left = 0
        sum_right = 0
        if leftbound <= mid:
            sum_left = self.__findSum(leftbound, min(mid, rightbound), node.left)
        if rightbound > mid:
            sum_right = self.__findSum(max(leftbound, mid + 1), rightbound, node.right)
        return sum_left + sum_right

    def __update(self,leftbound,rightbound,node,value):
        #if pending updates, update first
        if node.lazy:
            node.sum += (node.rightbound - node.leftbound +1)*node.lazy
            node.minimum += node.lazy
            if node.leftbound != node.rightbound:
                node.left.lazy = node.lazy
                node.right.lazy = node.lazy
            else:
                self.array[node.leftbound] += node.lazy
            node.lazy = 0

        #node is contained in interval
        if leftbound <= node.leftbound and rightbound >= node.rightbound:
            node.sum = (node.rightbound - node.leftbound + 1)*value
            node.minimum += value
            if node.leftbound == node.rightbound:
                self.array[node.leftbound] += value
            if node.right:
                node.right.lazy += value
            if node.left:
                node.left.lazy += value
            return
        
        #node is not contained in interval
        mid = (node.leftbound + node.rightbound)//2
        if leftbound <= mid:
            self.__update(leftbound, min(mid,rightbound), node.left,value)
        if rightbound > mid:
            self.__update(max(leftbound, mid+1), rightbound, node.right,value)
        node.sum = node.left.sum + node.right.sum
        node.minimum = min(node.left.minimum, node.right.minimum)
        


    def __str__(self):
        return self.root.__str__()
    
    def __repr__(self):
        return self.__str__()