# PRIME

** ARCHIVED PROJECT - NO LONGER MAINTAINED **

This repository contains the PRIME (Post-Refinement and Integration for Macromolecular Experiments) package, originally part of the [cctbx_project](https://github.com/cctbx/cctbx_project).

## Status

This project has been archived and is no longer actively maintained or developed. It is kept online for:
- Historical reference
- Existing users who may still depend on it
- Weekly automated testing to ensure it continues to build and run

No new features, bug fixes, or improvements are planned.

## Installation

```
git clone https://github.com/dwpaley/prime.git
cd prime
conda env create -f conda_env.yml
conda activate prime_base
pip install -e .
```

## Testing

See `.github/workflows/build_test.yml` for a test procedure using `xfel_regression`.

## License

This project inherits its license from the cctbx_project. See [LICENSE.txt](LICENSE.txt) for details.
