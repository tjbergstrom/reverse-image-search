# merge_imgs.py
# May 2021
# Remove duplicates from two directories of images.
# And optionally merge the two directories into one new dir.
#
# python3 merge_imgs.py -m path/to/imageset1 -n path/to/imageset2
# And -d is optional, if you want to combine and save the two sets into a new dir.
# Else the two sets stay saved where they are, with no duplicates between them.
#
# Notes:
# Let m be the length of the longer dataset, and n the length of the other.
# - Runtime is linear, O(m+n).
# - If both sets contain all the same images, then the second set will be completely removed.


import numpy as np
import argparse
import cv2
import sys
import os


def list_imgs(base):
	img_paths = []
	exts = set(['.jpg', '.jpeg', '.png', '.bmp'])
	for root, dirs, filenames in os.walk(base):
		for filename in filenames:
			ext = os.path.splitext(filename)[1]
			if ext in exts:
				img_paths.append(os.path.join(root, filename))
	return img_paths


def gen_hashes(img_paths, hash_size=8):
	hashes = {}
	for img_path in img_paths:
		img = cv2.imread(img_path)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.resize(img, (hash_size + 1, hash_size))
		diff = img[:, 1:] > img[:, :-1]
		img_hash = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
		paths = hashes.get(img_hash, [])
		paths.append(img_path)
		hashes[img_hash] = paths
	return hashes


def rm_dups(hashes):
	for img_hash, hashed_paths in hashes.items():
		if len(hashed_paths) > 1:
			for path in hashed_paths[1:]:
				os.remove(path)
	return hashes


def save_imgs(savedir):
	os.system(f"mkdir -p {savedir}")
	img_paths = set()
	for img_hash, hashed_paths in hashes.items():
		hashed_path = hashed_paths[0]
		img = cv2.imread(hashed_path)
		basename = os.path.basename(hashed_path)
		filename, ext = os.path.splitext(basename)
		img_path = os.path.join(savedir, basename)
		i = 1
		while img_path in img_paths:
			img_path = f"{savedir}/{filename}_{i}{ext}"
			i += 1
		cv2.imwrite(img_path, img)
		img_paths.add(img_path)


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-m", "--imgset1", required=True)
	ap.add_argument("-n", "--imgset2", required=True)
	ap.add_argument("-s", "--savedir", required=False)
	args = vars(ap.parse_args())

	# O(m+n)
	img_paths = list_imgs(args["imgset1"])
	img_paths += list_imgs(args["imgset2"])
	if len(img_paths) <= 0:
		sys.exit("No images found")

	# O(m+n)
	hashes = gen_hashes(img_paths)

	# O(m+n)
	hashes = rm_dups(hashes)

	# O(m+n)
	if args["savedir"]:
		save_imgs(args["savedir"])



##
