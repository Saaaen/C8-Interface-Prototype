from setuptools import setup, find_packages

setup(
    name='C8InterfacePrototype',  # Replace with your package's name
    version='0.1',  # The initial release version
    author='Saen Chen',  # Optional: your name or your organization's name
    author_email='saenc2@berkeley.edu',  # Optional: your email address
    description='A prototype of C8 Interface',  # Optional: a short description of the package
    url='https://github.com/Saaaen/C8-Interface-Prototype',  # Optional: the project home page
    packages=find_packages(),  # Automatically find and include all packages
    classifiers=[
        'Development Status :: 3 - Alpha',  # Change as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Change as appropriate
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',  # Minimum version requirement of the package
    install_requires=[
        # List your project's dependencies here, e.g.,
        'openai==0.28.1',
        'pyautogen'
    ],
)
