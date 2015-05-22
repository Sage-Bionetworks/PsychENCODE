dbFinder code for Shula et al data
==================================

The code available here reproduces the results presented by Andrew Jaffe at the conference call of 2015-May-15 for identifying differentially bounded regions with the Shula et al 2013 data by running [derfinder](http://bioconductor.org/packages/derfinder/). `derfinder` is described at

    Collado-Torres L, Frazee AC, Love MI, Irizarry RA, Jaffe AE, Leek JT. derfinder: Software for annotation-agnostic RNA-seq differential expression analysis. bioRxiv 015370 (2015). doi:10.1101/015370.
    

The analysis used a data cutoff of 2, models that adjusted for sample depth and tested for a linear effect in age in years, an F-statistic cutoff corresponding to a p-value of 0.01, and 100 permutations. Only the Neun+ samples were used in this analysis. For age in PCW, we used the following formula to get the age in years:

    age_in_years = (age_in_pcw - 42) / 52

The code in this repository is based on the code described in the `derfinder` supplementary website: [leekgroup.github.io/derSoftware/](http://leekgroup.github.io/derSoftware/). We highly recommend reading the `derfinder` [pre-print](http://biorxiv.org/content/early/2015/02/19/015370), the vignettes under the Bioconductor `derfinder` [page](http://bioconductor.org/packages/derfinder/), and the [supplementary website](http://leekgroup.github.io/derSoftware/). To reproduce the analysis note that you have to first download the BED files, you will need to change the paths in the scripts to match your setup, and you might need to change the bash scripts to match your cluster setup (ours uses SGE to manage the jobs queue).

Some important differences between this code and the one at the [supplementary website](http://leekgroup.github.io/derSoftware/) are outlined below:

* There is no `step1` script because the Shula et al 2013 data is available in BED format. Thus a custom script was used to load and format the data appropriately. See the scripts at [shula/CoverageInfo/](shula/CoverageInfo) for details.
* The analysis ends at the step of creating the derfinderReport with [regionReport](http://bioconductor.org/packages/regionReport). So there are no scripts for steps 6 and beyond.

If you have questions about `derfinder`, we recommend posting the questions at the Bioconductor Support [website](https://support.bioconductor.org/) using the `derfinder` tag.

Contact: Andrew Jaffe <andrew.jaffe@libd.org>.
