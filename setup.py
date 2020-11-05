import setuptools

setuptools.setup(
    name="VkBotWrapper", # Replace with your own username
    version="1.0.0",
    author="Chernenko Ruslan",
    author_email="ractyfree@gmail.com",
    description="A wrapper for vk_api library",
    url="https://github.com/ractyfree/vkBotWRP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)