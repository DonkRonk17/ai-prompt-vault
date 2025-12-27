from setuptools import setup

setup(
    name="ai-prompt-vault",
    version="1.0.0",
    description="Save, organize, search, and reuse your best AI prompts",
    author="Randell Logan Smith",
    author_email="logan@metaphysicsandcomputing.com",
    url="https://github.com/DonkRonk17/ai-prompt-vault",
    py_modules=["prompt_vault"],
    entry_points={
        "console_scripts": [
            "prompt-vault=prompt_vault:main",
            "pv=prompt_vault:main",
        ],
    },
    python_requires=">=3.8",
    extras_require={
        "clipboard": ["pyperclip"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)

