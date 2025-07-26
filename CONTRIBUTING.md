# Contributing to the OCPI EMSP-CPO Platform

First off, thank you for considering contributing to this project! Your help is greatly appreciated.

## Git Workflow

This project uses the [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branching model. The main branches are:

- `main`: This branch contains production-ready code. All development should be done in separate branches.
- `develop`: This is the main development branch. It contains the latest delivered development changes for the next release.

### Feature Branches

All new features should be developed in their own branches. These branches are created from `develop`.

- **Branch Naming Convention:** `feature/<short-description>`
- **Example:** `feature/ocpi-locations-endpoint`

When a feature is complete, it is merged back into `develop` through a pull request.

### Release Branches

When the `develop` branch has acquired enough features for a release, a `release` branch is created from `develop`.

- **Branch Naming Convention:** `release/<version-number>`
- **Example:** `release/v1.2.0`

No new features should be added to this branch. Only bug fixes, documentation generation, and other release-oriented tasks should go in this branch. Once it's ready, the `release` branch is merged into `main` and `develop`.

### Hotfix Branches

If a critical bug is found in `main`, a `hotfix` branch is created from `main` to fix it.

- **Branch Naming Convention:** `hotfix/<short-description>`
- **Example:** `hotfix/auth-bug-fix`

Once the fix is complete, the `hotfix` branch is merged into both `main` and `develop`.

## Pull Request Process

1.  Ensure your branch is up-to-date with `develop`.
2.  Create a pull request from your `feature` branch to `develop`.
3.  Fill out the pull request template with a clear description of your changes.
4.  Ensure all CI checks pass.
5.  At least one other developer must review and approve the pull request.
6.  Once approved, the pull request can be merged.

## Commit Message Guidelines

Please follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issues and pull requests liberally after the first line.

**Example:**

```
feat: Add support for OCPI 2.2.1 locations

This commit adds the necessary endpoints and data models to support the
locations module of the OCPI 2.2.1 specification.

Fixes #42
