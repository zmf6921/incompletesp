Implementation of the consecutive-ones approach for determining if a given preference profile of incomplete votes is single-peaked from "Incomplete Preferences in Single-Peaked Electorates" by Zack Fitzsimmons and Martin Lackner (https://arxiv.org/abs/1907.00752).

## Requires

- PreflibTools version 1.5.(https://github.com/nmattei/PrefLib-Tools)
- tryalgo development version (as of January 3, 2019). (https://github.com/jilljenn/tryalgo)

## Usage

    python3 weakorder-sp.py profile.toc N

where `profile.toc` is a preference profile in the tied-order complete format used by the PrefLib repository (www.preflib.org) and N is one of the following values.

0. To check if `profile.toc` describes a possibly single-peaked profile.
1. To check if `profile.toc` describes a single-plateaued profile.
2. To check if `profile.toc` describes a Black single-peaked profile.

### Example Instances
Four example preference profiles in the tied-order complete format used by PrefLib are included in the "examples" directory.
- `possibly-sp.toc` is possibly single-peaked
- `single-plateaued.toc` is single-plateaued and so also possibly single-peaked.
- `Black-sp.toc` is Black single-peaked and so also single-plateaued and possibly single-peaked.
- `none.toc` is not possibly single-peaked, single-plateaued, or Black single-peaked.

### Output

For a given input profile `profile.toc`, the output is four comma-separated values: the input profile filename, the number of candidates in the profile, the number of voters in the profile, and True if the given restriction is satisfied (False otherwise).

For example, testing the `possibly-sp.toc` profile with the command
```
python3 possibly-sp.toc 0
```
results in the following output.
```
possibly-sp.toc,6,4,True
```
