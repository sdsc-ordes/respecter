#!/usr/bin/env bash
set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`

# Default recipe to list all available recipes
default:
  just --list

# Setup development environment
setup:
  @echo "Setting up dependencies"
  uv venv
  bash -c ". .venv/bin/activate && uv sync --all-extras && exec ${SHELL:-bash}"
