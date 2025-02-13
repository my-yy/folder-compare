from natsort import natsorted, ns


# https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort

def sort_files(x):
    # 函数会返回一个新列表，不会影响原始列表的顺序
    return natsorted(x, key=lambda y: y.lower())


if __name__ == "__main__":
    x = ['Elm11', 'Elm12', 'Elm2', 'elm0', 'elm1', 'elm10', 'elm13', 'elm9']

    x = ["01_2", "01_1", "01_3"]
    print(sort_files(x))
