## 0.0.10 (2024/12/31)

- Address incompatibility with FileLock 3.15.3 causing the timeout parameter to
  be ignored.

## 0.0.9 (2023/10/30)

- Declare package incompatible with filelock 3.13.0. The problematic code was
  fixed upstream in the released version 3.13.1.

## 0.0.8 (2023/10/30)

- Fix compatibility with filelock 3.13.0.

## 0.0.7 (2023/04/18)

- Fix compatibility with filelock 3.12.0.
- multiuserfilelock (all version) are incompatible with filelock 3.11.0.

## 0.0.5 (2021/11/23)

- Ensure windows tests pass.

## 0.0.3 (2021/10/30)

- Ensure `tmpdir` is a `pathlib.Path`.
