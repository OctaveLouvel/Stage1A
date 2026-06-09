from setuptools import find_packages, setup

package_name = 'pose_to_moveit'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='auguste',
    maintainer_email='claudechristian.louvel@ensiie.eu',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'pose_to_moveit_node = pose_to_moveit.pose_to_moveit_node:main',
    ],
},
)
