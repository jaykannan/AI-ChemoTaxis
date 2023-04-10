from enums import Dir
from spacepartition import SpacePartition


class PartitionManager:
    def __init__(self, gd):
        self.Partitions = []

        WIDTH = 10
        HEIGHT = 8

        width = gd.get_viewport().width // PartitionManager.WIDTH
        height = gd.get_viewport().height // PartitionManager.HEIGHT

        # initialize partitions
        for j in range(PartitionManager.HEIGHT):
            for i in range(PartitionManager.WIDTH):
                temp = SpacePartition()
                temp.Bounds.x = int(i * width)
                temp.Bounds.y = int(j * height)
                temp.Bounds.width = width
                temp.Bounds.height = height
                temp.ID = len(self.Partitions)

                temp.Neighbour[Dir.TOP.value] = self.GetPartitionId(gd, temp.Bounds.center.x, temp.Bounds.y - height)
                temp.Neighbour[Dir.TOP_RIGHT.value] = self.GetPartitionId(gd, temp.Bounds.center.x + width, temp.Bounds.y - height)
                temp.Neighbour[Dir.RIGHT.value] = self.GetPartitionId(gd, temp.Bounds.center.x + width, temp.Bounds.y)
                temp.Neighbour[Dir.BOTTOM_RIGHT.value] = self.GetPartitionId(gd, temp.Bounds.center.x + width, temp.Bounds.y + height)
                temp.Neighbour[Dir.BOTTOM.value] = self.GetPartitionId(gd, temp.Bounds.center.x, temp.Bounds.y + height)
                temp.Neighbour[Dir.BOTTOM_LEFT.value] = self.GetPartitionId(gd, temp.Bounds.center.x - width, temp.Bounds.y + height)
                temp.Neighbour[Dir.LEFT.value] = self.GetPartitionId(gd, temp.Bounds.center.x - width, temp.Bounds.y)
                temp.Neighbour[Dir.TOP_LEFT.value] = self.GetPartitionId(gd, temp.Bounds.center.x - width, temp.Bounds.y - height)

                self.Partitions.append(temp)
    
        def GetPartitionId(gd, x, y):
            if x < 0 or y < 0:
                return -1
            if x >= gd.Viewport.Width or y >= gd.Viewport.Height:
                return -1
            
            a = int((x / gd.Viewport.Width) * WIDTH)
            b = int((y / gd.Viewport.Height) * HEIGHT)
            
            return (b * WIDTH) + a
