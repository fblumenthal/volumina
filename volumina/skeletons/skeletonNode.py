from PyQt4.QtCore import QPointF, QObject, pyqtSignal
from PyQt4.QtGui import QColor

class SkeletonNode(QObject):
    selected = pyqtSignal(bool)

    def __init__(self, pos3D, axis, skeletons):
        super(SkeletonNode, self).__init__()

        from volumina.skeletons import Skeletons
        assert isinstance(skeletons, Skeletons)
        assert len(pos3D) == 3
        assert axis in [0,1,2]

        self.pos = pos3D
        self.shape = [6,6,6]
        self.axis = axis
        self._skeletons = skeletons
        self._selected = False
        self._isMovable = True
        self._color = QColor(0,0,255)
        self._name = "unnamed node"

    def setColor(self, c):
        self._color = c

    def setName(self, name):
        self._name = name

    def name(self):
        return self._name

    def color(self):
        return self._color

    def isMovable(self):
        return self._isMovable

    def setMovable(self, movable):
        self._isMovable = movable
    
    def __str__(self):
        return "SkeletonNode(pos=%r, axis=%r)" % (self.pos, self.axis)

    def __repr__(self):
        return "SkeletonNode(pos=%r, axis=%r)" % (self.pos, self.axis)

    def move(self, pos):
        self.pos = pos
        
    def intersectsBbox(self, point):
        assert len(point) == 3
        for i in range(3):
            if not (self.pos[i] - self.shape/2.0 >= point[i] and self.pos[i] + self.shape/2.0 <= point[i]):
                return False 
        return True

    def shape2D(self, axis):
        shape = list(self.shape)
        del shape[axis]
        return shape
    
    def setNewShape(self, axis, newShape):
        self.shape[axis] = newShape

    def pointF(self, axis=None):
        if axis is None:
            axis = self.axis
        pos2D = list(self.pos)
        del pos2D[axis]
        return QPointF(*pos2D)

    def setSelected(self, selected):
        if self._selected == selected:
            return
        self._selected = selected
        self.selected.emit(self._selected)

    def isSelected(self):
        return self._selected
