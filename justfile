#!/usr/bin/env bash
set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`

# Default recipe to list all available recipes
default:
  just --list

# Setup development dependencies
install:
  @echo "Setting up dependencies"
  uv venv
  uv sync --all-extras --group={'dev','test'}

# Enter development shell
dev: install
  @echo "Entering venv..."
  bash -c ". .venv/bin/activate && exec ${SHELL:-bash}"

# Run unit tests
test:
  @echo "Running tests"
  uv run pytest
