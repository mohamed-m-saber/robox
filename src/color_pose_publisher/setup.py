import os
from setuptools import setup

package_name = 'color_pose_publisher'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    py_modules=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install assets
        (os.path.join('share', package_name, 'assets'), [
            os.path.join(package_name, 'assets', 'camera_calibration_data.npz'),
            os.path.join(package_name, 'assets', 'test.jpg'),
            os.path.join(package_name, 'assets', 'workspace.png'),
        ]),
    ],
    install_requires=['setuptools', 'cube_msgs'],
    zip_safe=True,
    maintainer='Saber',
    maintainer_email='saber@example.com',
    description='ROS 2 Python package for detecting colored cubes and publishing pose + color',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'color_pose_publisher_node = color_pose_publisher.color_pose_publisher_node:main',
            'ppc_action_client = color_pose_publisher.ppc_action_client:main',
            'color_tracking_pub = color_pose_publisher.color_tracking_pub:main',
            'qr_action_client = color_pose_publisher.qr_action_client:main',



        ],
    },
)




