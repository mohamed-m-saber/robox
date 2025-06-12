from setuptools import find_packages, setup

package_name = 'arduinobot_py_examples'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saber',
    maintainer_email='saber@todo.todo',
    description='Python examples for Arduino-based robot using ROS 2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher = arduinobot_py_examples.publisher:main',
            'subscriber = arduinobot_py_examples.subscriber:main',
            'joystick_handler = arduinobot_py_examples.joystick_handler:main',
            'simple_parameter = arduinobot_py_examples.simple_parameter:main',
            
            'serial = arduinobot_py_examples.serial:main',
            'bridge = arduinobot_py_examples.bridge:main',
            'pose = arduinobot_py_examples.pose:main',
            'simple_moveit_interface = arduinobot_py_examples.simple_moveit_interface:main',
            'ik_solver = arduinobot_py_examples.ik_solver:main'


            
            
        ],
    },
)

