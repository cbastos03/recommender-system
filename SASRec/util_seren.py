# Copyright (c) Recommenders contributors.
# Licensed under the MIT License.

from collections import defaultdict


class SASRecDataSet:
    """
    A class for creating SASRec specific dataset used during
    train, validation and testing.

    Attributes:
        usernum: integer, total number of users
        itemnum: integer, total number of items
        User: dict, all the users (keys) with items as values
        Items: set of all the items
        user_train: dict, subset of User that are used for training
        user_valid: dict, subset of User that are used for validation
        user_test: dict, subset of User that are used for testing
        col_sep: column separator in the data file
        filename: data filename
    """

    def __init__(self, **kwargs):
        self.usernum = 0
        self.itemnum = 0
        self.User = defaultdict(list)
        self.Items = set()
        self.user_train = {}
        self.user_valid = {}
        self.user_test = {}
        self.serendipity = defaultdict(dict)  # New dictionary to store serendipity values
        self.col_sep = kwargs.get("col_sep", " ")
        self.filename = kwargs.get("filename", None)

        if self.filename:
            with open(self.filename, "r") as fr:
                sample = fr.readline()
            ncols = len(sample.strip().split(self.col_sep))
            if ncols == 3:
                self.with_time = True
            elif ncols == 2:
                self.with_time = False
            else:
                raise ValueError(f"3 or 2 columns must be in dataset. Given {ncols} columns")

    def split(self, **kwargs):
        self.filename = kwargs.get("filename", self.filename)
        if not self.filename:
            raise ValueError("Filename is required")

        self.data_partition()

    def data_partition(self):
        # assume user/item index starting from 1
        f = open(self.filename, "r")
        for line in f:
            u, i, s = line.rstrip().split(self.col_sep)
            u = int(u)
            i = int(i)
            s = int(float(s))
            self.usernum = max(u, self.usernum)
            self.itemnum = max(i, self.itemnum)
            self.User[u].append(i)
            self.serendipity[u][i] = s

        for user in self.User:
            nfeedback = len(self.User[user])
            if nfeedback < 3:
                self.user_train[user] = self.User[user]
                self.user_valid[user] = []
                self.user_test[user] = []
            else:
                self.user_train[user] = self.User[user][:-2]
                self.user_valid[user] = []
                self.user_valid[user].append(self.User[user][-2])
                self.user_test[user] = []
                self.user_test[user].append(self.User[user][-1])
