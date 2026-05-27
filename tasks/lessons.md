# Lessons learned

Short notes from incidents, reviews, or retro sessions. **Bullets only**; link tickets or PRs when relevant.

- Container-only rule is strict: if a ticket lacks a Docker/Dev Container command path for TEST/DEV/VAL, add one first (for FR-0002 web, `./develop web ...`) before running validation.
- For package work inside submodules such as Kindling Mantle, run installs/tests/pack checks inside the project Docker tooling container and activate the required package manager there with Corepack; host-local package-manager validation is not acceptable evidence.
