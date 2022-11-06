# Cancer_Finder

## Documentation

### Intro

- The app consists of two parts, back (Cancer_Finder repo) and front(Cancer_Finder_F repo)
- Back provides functionality:
    - neural network, which can generate defects on healthy CT image and save them on server
    - contains dcm images original CT
    - contains dcm images segmentation
    - provide access to CT images from front and get new segmentation from front

- Front provides functionality:
    - Get CT image and show as image in redactor
    - Segmentation redactor and save it to server

### Back

- There are 4 main models and 3 script to use:
    - Modules:
        - utils - contains nii2dcm.py module with functions of nifti to dicom converter
        - ImageWork = contains modules of transformation from grey scale of dicom to RGB, BGR and back, which all used
          in
          processing of images to receive, send and contain images
        - DataBase - contains Mongo database api usage, to save and load images
        - nn - module contains modules of experiments (VAE and UNET in module name), and main model of generation - GAN.
          Other code is inference and train modules (contains it in modules names), and api module, which contains main
          functions of usage:
          load_model, inference, train. The last group of modules is dataloder modules
    - Scripts:
        - app.py - the main script of starting the back
        - cuda.py - script of check cuda-toolkit availability and machine resources
        - test.py - used in development process to check work of parts of app