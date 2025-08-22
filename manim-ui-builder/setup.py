from setuptools import setup, find_packages

setup(
    name="manim-ui-builder",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A visual editor for Manim animations with Gemini Pro integration.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/manim-ui-builder",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5",  # or PySide2 if you prefer
        "manim",  # Manim Community Edition
        "fastapi",  # For backend API
        "httpx",  # For making HTTP requests to Gemini API
        "python-dotenv",  # For loading environment variables
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)