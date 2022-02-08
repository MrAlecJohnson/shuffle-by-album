from setuptools import find_packages, setup

setup(
    name="shuffle-by-album",
    packages=find_packages(),
    version="0.0.1",
    description="Spotify web app to pick random albums from a playlist of songs.",
    python_requires=">=3.9.6",
    author="Alec Johnson",
    license="MIT",
    install_requires=["pytest     ~=7.0.0", "pyyaml     ~=6.0", "spotipy    ~=2.19.0"],
)
