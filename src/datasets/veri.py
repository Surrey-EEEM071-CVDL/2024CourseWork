# Copyright (c) EEEM071, University of Surrey

import glob
import os.path as osp
import re

from .base import BaseImageDataset


class VeRi(BaseImageDataset):
    """
    VeRi
    Reference:
    Liu, X., Liu, W., Ma, H., Fu, H.: Large-scale vehicle re-identification in urban surveillance videos. In: IEEE   %
    International Conference on Multimedia and Expo. (2016) accepted.

    Dataset statistics: Total images
    # identities: 776 vehicles(576 for training and 200 for testing)
    # images: 37778 (train) + 11579 (query)
    """

    dataset_dir = "VeRi"

    def __init__(self, root="datasets", verbose=True, **kwargs):
        super().__init__(root)
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, "image_train")
        self.query_dir = osp.join(self.dataset_dir, "image_query")
        self.gallery_dir = osp.join(self.dataset_dir, "image_test")

        self.check_before_run()

        train = self.process_dir(self.train_dir, relabel=True)
        query = self.process_dir(self.query_dir, relabel=False)
        gallery = self.process_dir(self.gallery_dir, relabel=False)

        if verbose:
            print("=> VeRi loaded")
            self.print_dataset_statistics(train, query, gallery)

        self.train = train
        self.query = query
        self.gallery = gallery

        (
            self.num_train_pids,
            self.num_train_imgs,
            self.num_train_cams,
        ) = self.get_imagedata_info(self.train)
        (
            self.num_query_pids,
            self.num_query_imgs,
            self.num_query_cams,
        ) = self.get_imagedata_info(self.query)
        (
            self.num_gallery_pids,
            self.num_gallery_imgs,
            self.num_gallery_cams,
        ) = self.get_imagedata_info(self.gallery)

    def check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError(f'"{self.dataset_dir}" is not available')
        if not osp.exists(self.train_dir):
            raise RuntimeError(f'"{self.train_dir}" is not available')
        if not osp.exists(self.query_dir):
            raise RuntimeError(f'"{self.query_dir}" is not available')
        if not osp.exists(self.gallery_dir):
            raise RuntimeError(f'"{self.gallery_dir}" is not available')

    '''
    Read images as per the file names mentioned in corresponding text files
    name_train.txt, name_query.txt, name_test.txt
    '''
    def process_dir(self, dir_path, relabel=False):
        img_paths = []
        with open(osp.join(self.dataset_dir, "name_" + dir_path.split("_")[-1] + ".txt"), "r") as file:
            for image_name in file:
                image_name = image_name.rstrip()
                img_paths.append(osp.join(dir_path, image_name))
        pattern = re.compile(r"([-\d]+)_c([-\d]+)")

        pid_container = set()
        for img_path in img_paths:
            pid, _ = map(int, pattern.search(img_path).groups())
            if pid == -1:
                continue  # junk images are just ignored
            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        dataset = []
        for img_path in img_paths:
            pid, camid = map(int, pattern.search(img_path).groups())
            if pid == -1:
                continue  # junk images are just ignored
            assert 0 <= pid <= 1501  # pid == 0 means background
            assert 1 <= camid <= 20
            camid -= 1  # index starts from 0
            if relabel:
                pid = pid2label[pid]
            dataset.append((img_path, pid, camid))

        return dataset
