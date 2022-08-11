import sys
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QTimeLine
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QLabel, QGraphicsItemAnimation
from PySide6.QtGui import QPixmap, QTransform

app = QApplication(sys.argv)

# Create window with gray background
scene = QGraphicsScene(0, 0, 800, 480)
scene.setBackgroundBrush(Qt.gray)

# Create reel image
pixmap = QPixmap("img/tape_reel.png")
pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

# add images to scene
reel1 = scene.addPixmap(pixmap)
reel1.setPos(30, 20)

reel2 = scene.addPixmap(pixmap)
reel2.setPos(470, 20)

t = QTransform()
center = reel2.boundingRect().center()
t.translate(center.x(), center.y())
t.rotate(70)
t.translate(-center.x(), -center.y())
reel2.setTransformationMode(Qt.SmoothTransformation)
reel2.setTransform(t)

timer = QTimeLine(5000)
timer.setFrameRange(0, 100)
animation = QGraphicsItemAnimation()
animation.setItem(reel1)
animation.setTimeLine(timer)

for i in range(180):
	animation.setRotationAt(i/180, i)

# Display window
view = QGraphicsView(scene)
view.show()

sys.exit(app.exec())

