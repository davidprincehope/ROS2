from setuptools import find_packages, setup

package_name = 'led_man_pkg'

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
    maintainer='davidprincehope',
    maintainer_email='lanresmail410@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "led_client = led_man_pkg.led_client_node:main",
            "led_panel = led_man_pkg.led_panel_node:main"
        ],
    },
)
