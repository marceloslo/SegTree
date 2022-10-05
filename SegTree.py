
class SegNode:
    def __init__(self, leftbound, rightbound, sum, minimum):
        self.leftbound = leftbound
        self.rightbound = rightbound
        self.minimum = minimum
        self.sum = sum
        self.left = None
        self.right = None
        
class SegTree:
    def __init__(self, array):
        self.root = self.construct(array,0,len(array)-1)
        self.array = array

    def construct(self,array,leftbound,rightbound):
        if(leftbound == rightbound):
            return SegNode(leftbound, rightbound, array[leftbound], array[leftbound])
        no = SegNode(leftbound, rightbound, -1, -1)
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
        if leftbound == node.leftbound and rightbound == node.rightbound:
            return node.sum
        mid = (node.leftbound + node.rightbound)//2
        sum_left = 0
        sum_right = 0
        if leftbound <= mid:
            sum_left = self.__findSum(leftbound, min(mid,rightbound), node.left)
        if rightbound > mid:
            sum_right = self.__findSum(max(leftbound, mid+1), rightbound, node.right)
        return sum_left + sum_right

    def __update(self,leftbound,rightbound,node,value):
        #if leaf, update values
        if node.leftbound==node.rightbound:
            node.sum += value
            node.minimum = node.sum
            self.array[leftbound] = node.sum
            return
        #else
        mid = (node.leftbound + node.rightbound)//2
        #update children
        if leftbound <= mid:
            self.__update(leftbound, min(mid,rightbound),node.left,value)
        if rightbound > mid:
            self.__update(max(leftbound, mid+1), rightbound, node.right,value)
        
        #update node values
        node.sum = node.left.sum + node.right.sum
        node.minimum = min(node.left.minimum,node.right.minimum)
        return
        
    def __str__(self):
        return self.root.__str__()
    
    def __repr__(self):
        return self.__str__()