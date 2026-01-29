#!/bin/bash

# This script automates the process of setting up a Jekyll site
# and deploying it to GitHub Pages.

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if Jekyll is already installed
if ! command -v jekyll &> /dev/null
then
    echo "Jekyll is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y ruby-full build-essential zlib1g-dev
    sudo gem install jekyll bundler
else
    echo "Jekyll is already installed."
fi

# Set the repository name and username
REPO_NAME="agdr"
USERNAME="Archidiot"

# Check if the directory exists
if [ ! -d "$REPO_NAME" ]; then
    echo "Creating new Jekyll site..."
    jekyll new $REPO_NAME
else
    echo "Jekyll site already exists."
fi

# Go to the directory
cd $REPO_NAME

# Add some content for testing purposes
echo "Hello world" > index.html

# Initialize a git repository if it doesn't exist
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add . 
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/$USERNAME/$REPO_NAME.git
else
    echo "Git repository already initialized."
fi

# Set up git credentials using token
TOKEN=$(grep GITHUB_API_KEY ../.env | cut -d '=' -f2)
git remote set-url origin https://$TOKEN@github.com/$USERNAME/$REPO_NAME.git

# Push the changes
echo "Pushing to GitHub Pages..."
git push -f origin main

# Output the URL for the website
echo "Successfully deployed to https://$USERNAME.github.io/$REPO_NAME/"
