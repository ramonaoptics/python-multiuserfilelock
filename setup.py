from setuptools import find_packages, setup
import versioneer


setup(
    name='multiuserfilelock',
    version=versioneer.get_version(),
    url='https://github.com/ramonaoptics/python-multiuserfilelock',
    author='Ramona Optics, Inc.',
    author_email='info@ramonaoptics.com',
    description='A lock to share resources between users based on filelock.',
    license='BSD',
    python_requires='>=3.7',
    install_requires=[
        'filelock',
    ],
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
)
