import setuptools


__version__ = "0.0.1"

REPO_NAME = "Automated-Storyboard-Synthesis-for-Digital-Advertising"
AUTHOR_USER_NAME = "azizadx"
SRC_REPO = "Automated-Storyboard-Synthesis-for-Digital-Advertising"
AUTHOR_EMAIL = "craft@azizadx.me"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="This transformation process aims to visually depict the narrative flow and user interaction within advertisements, making the conceptualization of digital campaigns both more intuitive and impactful.",
    # long_description='Redash LLM Chatbot: AI-powered Analytics &amp; Insights Unlock the power of your Redash dashboards and databases with natural language queries and automated insights.',
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
