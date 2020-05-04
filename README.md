# jpAutograderComps

looks like most of this is moved to datascience-in github repos. The autgradre parts still need to be absorbed from repos admin/uu/...*AppliedStats*2019...
When that is done delte this repository...

This is a repository for various components developed around semi/auto-grading a jupyter .ipynb notebook

# Pure Jupyter `.ipynb` Notebooks

The following two spteps for SageMath can be followed for a pure Python `.ipynb` notebook running in a jupyter notebook server.

# SageMath `.ipynb` Jupyter Notebooks

This Dockerised environment for SageMath is part of the auto-grader component for an [Applied Statistics Course](https://lamastex.github.io/scalable-data-science/as/2019/).
  
Use the Makefile as follows:

Terminal 1:
`make build` builds a new docker image from `sagemath/sagemath`.

`make run` runs the image so one can work with jupyter notebook by mounting the current directory.

Terminal 2:
Also you may want to run a plain sageMathbash docker to work in a pure sage bash environment. For this do:

- `make runSageMathBash` to get into another docker container
- `python makeAllNotesFromMaster.py`  # to generate all the student versions of .ipynb and assignment ? notebooks into `2019/jp/` from those in `master/jp/*.ipynb` as specified in `inputMasterNBNos` list in `makeAllNotesFromMaster.py`

