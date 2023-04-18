from setuptools import find_packages, setup
import versioneer

with open('README.md') as readme_file:
    readme = readme_file.read()


setup(
    name='multiuserfilelock',
    version=versioneer.get_version(),
    url='https://github.com/ramonaoptics/python-multiuserfilelock',
    author='Ramona Optics, Inc.',
    author_email='info@ramonaoptics.com',
    description='A lock to share resources between users based on filelock.',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='BSD',
    python_requires='>=3.7',
    install_requires=[
        'filelock!=3.11.0',
    ],
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
)
