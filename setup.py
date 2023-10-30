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
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'filelock!=3.11.0,!=3.13.0',
    ],
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
)
