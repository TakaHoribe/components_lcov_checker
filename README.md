# components_lcov_checker

Run lcov and make csv for each components

## how to use

Run the following command. The `components_coverage_results.csv` file will be generated for each component.

```sh
cd <YOUR AUTOWARE DIRECTORY>

git clone git@github.com:TakaHoribe/components_lcov_checker.git

colcon build --symlink-install --cmake-args \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DCMAKE_CXX_FLAGS=" --coverage" -DCMAKE_C_FLAGS=" --coverage"; 

colcon lcov-result --initial;
colcon test;
python3 ./components_lcov_checker/components_lcov_checker.py
```

All-in-one code:

```sh
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_CXX_FLAGS=" --coverage" -DCMAKE_C_FLAGS=" --coverage"; colcon lcov-result --initial; colcon test; python3 ./components_lcov_checker/components_lcov_checker.py
```


