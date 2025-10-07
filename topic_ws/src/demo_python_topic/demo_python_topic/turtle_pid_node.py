import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = 0.0
        self.integral = 0.0

    def compute(self, error):
        self.integral += error
        derivative = error - self.last_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error
        return output

class TurtlePIDNode(Node):
    def __init__(self):
        super().__init__('turtle_pid_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        # 用参数方程生成高密度爱心轨迹点
        self.target_points = []
        for t in [i * 0.05 for i in range(int(2 * math.pi / 0.05) + 1)]:
            x = 5.5 + 4 * math.sin(t) ** 3
            y = 5.5 + 3.5 * math.cos(t) - 1.5 * math.cos(2 * t) - 0.5 * math.cos(3 * t) - 0.2 * math.cos(4 * t)
            self.target_points.append((x, y))
        # 回到起点
        self.target_points.append(self.target_points[0])

        self.current_target_idx = 0
        self.pose = None
        self.pid_linear = PIDController(1.2, 0.0, 0.1)
        self.pid_angular = PIDController(10.0, 0.0, 2.0)

    def pose_callback(self, msg):
        self.pose = msg
        self.move_to_target()

    def move_to_target(self):
        if self.pose is None or self.current_target_idx >= len(self.target_points):
            return
        target_x, target_y = self.target_points[self.current_target_idx]
        dx = target_x - self.pose.x
        dy = target_y - self.pose.y
        distance = math.sqrt(dx**2 + dy**2)
        angle_to_target = math.atan2(dy, dx)
        angle_error = self.normalize_angle(angle_to_target - self.pose.theta)

        # PID控制
        linear_speed = self.pid_linear.compute(distance)
        angular_speed = self.pid_angular.compute(angle_error)

        # 到达目标点则切换下一个
        if distance < 0.05:
            self.current_target_idx += 1
            self.pid_linear.integral = 0
            self.pid_angular.integral = 0

        twist = Twist()
        twist.linear.x = max(min(linear_speed, 1.0), -1.0)
        twist.angular.z = max(min(angular_speed, 6.0), -6.0)
        self.publisher_.publish(twist)

    @staticmethod
    def normalize_angle(angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

def main(args=None):
    rclpy.init(args=args)
    node = TurtlePIDNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()