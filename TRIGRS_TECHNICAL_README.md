README
======

Description
-----------

The Transient Rainfall Infiltration and Grid-Based Regional Slope-Stability Model (TRIGRS) is a Fortran program designed for modeling the timing and distribution of shallow, rainfall-induced landslides. The program computes transient pore-pressure changes, and attendant changes in the factor of safety, due to rainfall infiltration. The program models rainfall infiltration, resulting from storms that have durations ranging from hours to a few days, using analytical solutions for partial differential equations that represent one-dimensional, vertical flow in isotropic, homogeneous materials for either saturated or unsaturated conditions. Use of step-function series allows the program to represent variable rainfall input, and a simple runoff routing model allows the user to divert excess water from impervious areas onto more permeable downslope areas. The TRIGRS program uses a simple infinite-slope model to compute factor of safety on a cell-by-cell basis. An approximate formula for effective stress in unsaturated materials aids computation of the factor of safety in unsaturated soils. Horizontal heterogeneity is accounted for by allowing material properties, rainfall, and other input values to vary from cell to cell. This command-line program is used in conjunction with geographic information system (GIS) software to prepare input grids and visualize model results.  

### Purpose and limitations ###

TRIGRS is a tool to be used by investigators who have some knowledge and experience concerning landslide behavior. Selecting input parameters and interpreting results requires geologic and engineering judgment.  The user should understand the theory and limitations behind TRIGRS, which are outlined in the documentation (Baum and others, 2002, 2008).  The user must also be aware of the limitations of the digital elevation model, physical properties and hydrologic data that TRIGRS uses as input for analyses.  

### Typical Workflow ###

At the beginning of a project, the user would prepare a digital elevation model, slope grid, flow-direction grid, and physical properties zone grid files using Geographic Information System (GIS) software.  Next, if needed, the user would run UnitConvert to put the grid files into a consistent system of units. Use GridMatch to ensure that the grid files are congruent.  A common source of errors running TRIGRS is grids that contain the same number of cells, but the number or locations of no-data cells differ slightly because they have been generated from different sources.  The user should then run TopoIndex using the digital elevation model and direction grid file as input to define the flow distribution pattern and compute weighting factors for distributing surface runoff.  Routing and distribution of surface runoff is optional; however, TopoIndex will compute array sizes from the digital elevation model to be used by TRIGRS, and so the user should run TopoIndex once at the beginning of a project to determine array sizes.  After preparing the topographic and physical properties data, converting the data to consistent units, computing array sizes and (if desired) preparing the flow distribution data, the project is ready for analysis using TRIGRS.  The user may configure TRIGRS to establish a time-series response of shallow pore water and stability of shallow slope deposits to rainfall infiltration.  Several initial runs of TRIGRS may be needed to verify calibration of the input parameters, the colluvial depth model and initial groundwater conditions.    

### What's included ###

This distribution includes source code files for the program TRIGRS and three companion utility programs, TopoIndex, GridMatch, and UnitConvert.  It also includes sample data in the data folder and sample initialization files in the main folder.  Empty folders for documentation, "doc" and executable binaries, "bin", are also included in the top-level directory.

### User Interface ###

TRIGRS and its companion utility programs, TopoIndex, GridMatch, and UnitConvert, run from the command line and have limited user interaction.  Each program uses an initialization file that contains basic data needed to run the program as well as the names of other input files.  

### Latest version (February 2022) ###

This release, 2.1.0c, includes bug fixes to correct errors in water table depth or elevation outputs as well as other minor adjustmnents.  Thus 2.1.0c is a minor update to 2.1.0a, which included new output formats and various optimizations to improve performance of the TRIGRS serial code.  These improvements have also been incorporated into a parallel implementation of the TRIGRS program (Alvioli and Baum, 2016).  We have parallelized the four time-demanding execution modes of TRIGRS, namely both the saturated and unsaturated model with finite and infinite soil depth options, within the Message Passing Interface (MPI) framework. Performance gain with respect to the serial code was tested both on commercial hardware and on a high-performance multi-node machine. We also compared results of the parallel code against results of the serial code for a large study area in Colorado to verify accuracy of the results.  

### Testing ###

Throughout its development, the code has passed through various kinds of testing to verify that it (1) reproduces results of the basic formulas for transient infiltration and slope stability and correctly maps grid cells to their spatial locations (Baum and others, 2002, 2008, 2010, 2013), (2) that it produces results that are consistent with actual case studies (Savage and others, 2003, 2005, Salciarini and others, 2006; Godt and others, 2008a, 2008b; Baum and others, 2010, 2011; Raia and others 2014; Gioia and others, 2015).  

References cited
----------------

*   Alvioli, Massimiliano, and Baum, R.L., 2016, Parallelization of the TRIGRS model for rainfall-induced landslides using the message passing interface: Environmental Modeling & Software, v. 81, p. 122-135, doi: 10.1016/j.envsoft.2016.04.002.

*   Baum, R.L., Savage, W.Z., and Godt, J.W., 2008, TRIGRS--A Fortran program for transient rainfall infiltration and grid-based regional slope-stability analysis, version 2.0: U.S. Geological Survey Open-File Report, 2008-1159, 75 p. https://doi.org/10.3133/ofr20081159
